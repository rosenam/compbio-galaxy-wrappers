
import vcfpy
from operator import attrgetter
from natsort import natsorted
import json

VERSION = '0.0.3'

# TODO: m2 vcf INFO ',' are converted to %2C; no ',' in fb INFO values


class VarLabel:
    """
    Label variant in a VCF
    """
    def __init__(self, input_vcf, label):
        self.reader = vcfpy.Reader.from_path(input_vcf)
        self.label = label

    def _get_dict_records(reader):
        records = {}
        for record in reader:
            var_id = '{}:{}{}>{}'.format(record.CHROM, record.POS, record.REF, record.ALT)
            if var_id not in records:
                records[var_id] = record
        return records

    def get_filter_records(self, exclusive, remove):
        """
        filter records with exclusively or inclusively a filter or a set of filters
        """
        selected = []
        removed = []
        for record in self.reader:
            if exclusive:
                if set(self.label) == set(record.FILTER):
                    selected.append(record)
                else:
                    removed.append(record)
            else:
                for lab in self.label:
                    if lab in record.FILTER:
                        selected.append(record)
                    else:
                        removed.append(record)
        if remove:
            return removed, selected
        else:
            return selected, removed

    def add_label_info(self, description):
        self.reader.header.add_filter_line(vcfpy.OrderedDict([('ID', self.label), ('Description', description)]))

    def label_records(self, resource):
        """
        Label records based on resource VCF
        """
        records = []
        resource = self._get_dict_records(vcfpy.Reader.from_path(resource))
        for record in self.reader:
            var_id = '{}:{}{}>{}'.format(record.CHROM, record.POS, record.REF, record.ALT)
            if var_id in resource:
                record.add_filter(self.label)
                records.append(record)
            else:
                records.append(record)
        return records


class VarFilter:
    """
    Filter records in a VCF based from an INFO field column and on a FORMAT field column
    """
    def __init__(self, input_vcf):
        self.reader = vcfpy.Reader.from_path(input_vcf)
        self.header = self.reader.header
        self.samples = self.reader.header.samples.names

    def filter_records(self, filter_from, filter_on, alt_allele):
        records_abovebkgd = []
        records_belowbkgd = []
        for record in self.reader:
            alt_type = record.ALT[0].type
            if alt_allele and alt_type == 'SNV':
                alt_str = '_' + record.ALT[0].value
            else:
                alt_str = ''
            f_on = filter_on + alt_str
            f_from = filter_from + alt_str
            if record.call_for_sample[self.samples[0]].data[f_on] > record.INFO[f_from]:
                records_abovebkgd.append(record)
            else:
                records_belowbkgd.append(record)
        return records_abovebkgd, records_belowbkgd


class VarWriter:
    """
    Write out records to a VCF
    """
    def __init__(self, records):
        self.records = records

    def as_vcf(self, output_vcf, header):
        writer = vcfpy.Writer.from_path(output_vcf, header=header)
        for record in natsorted(self.records, key=attrgetter('CHROM', 'POS')):
            writer.write_record(record)

    def as_json(self, output_json):
        with open(output_json, 'w') as oj:
            to_dump = {k: v for k, v in self.records.items()}
            oj.write(json.dumps(to_dump))


class VcfMerger:
    """
    Merge headers and variants in VCFs produced by different variant callers
    """
    # TODO: multi-sample instead of first vcf samples
    def __init__(self, input_vcfs, callers, vcf_format="VCFv4.2"):
        self.readers = [vcfpy.Reader.from_path(vcf) for vcf in input_vcfs]
        self.callers = callers
        self.samples = list(set([name for reader in self.readers for name in reader.header.samples.names]))
        self.filters = list(set(['{}_{}'.format(caller, flt) for reader, caller in zip(self.readers, self.callers) for flt in reader.header.filter_ids()]))
        self.infos = list(set(['{}_{}'.format(caller, info) for reader, caller in zip(self.readers, self.callers) for info in reader.header.info_ids()]))
        self.formats = list(set(['{}_{}'.format(caller, fmt) for reader, caller in zip(self.readers, self.callers) for fmt in reader.header.format_ids()]))
        self.header = vcfpy.Header(samples=[reader.header.samples for reader in self.readers][0])  #
        self.header.add_line(vcfpy.HeaderLine('fileformat', vcf_format))
        print(self.samples)

    def merge_headers(self):
        # using contig header from first sample only
        for contig in self.readers[0].header.get_lines('contig'):
            self.header.add_contig_line(vcfpy.OrderedDict([('ID', contig.id), ('length', contig.length)]))
        # add each caller to header as FILTER
        for reader, caller in zip(self.readers, self.callers):
            self.header.add_filter_line(vcfpy.OrderedDict([('ID', caller), ('Description', 'Variant caller label.')]))
        # add FILTER field info from each vcf to new header
        seen = []
        for reader, caller in zip(self.readers, self.callers):
            for flt in reader.header.get_lines('FILTER'):
                if flt.id not in seen:
                    seen.append(flt.id)
                    if flt.id not in ['.', 'PASS']:
                        self.header.add_filter_line(vcfpy.OrderedDict([('ID', flt.id),
                                                                       ('Description', flt.description)]))
        # add INFO field info from each vcf to new header
        for reader, caller in zip(self.readers, self.callers):
            for info in reader.header.get_lines('INFO'):
                self.header.add_info_line(vcfpy.OrderedDict([('ID', '{}_{}'.format(caller, info.id)),
                                                             ('Number', info.number), ('Type', info.type),
                                                             ('Description', '{} {}'.format(caller, info.description))]))
        # add FORMAT field info from each vcf to new header
        for reader, caller in zip(self.readers, self.callers):
            for fmt in reader.header.get_lines('FORMAT'):
                self.header.add_format_line(vcfpy.OrderedDict([('ID', '{}_{}'.format(caller, fmt.id)),
                                                               ('Number', fmt.number), ('Type', fmt.type),
                                                               ('Description', '{} {}'.format(caller, fmt.description))]))
        return self.header

    def merge_records(self):
        records = {}
        for reader, caller in zip(self.readers, self.callers):
            for record in reader:
                var_id = '{}:{}{}>{}'.format(record.CHROM, record.POS, record.REF, record.ALT)
                record.add_filter(caller)
                # for INFO and FORMAT ids, add caller as prefix, e.g m2_AD, fb_AD
                for info in self.infos:
                    record.INFO[info] = None
                    c, k = info.split('_', 1)
                    if c == caller:
                        record.INFO[info] = record.INFO.get(k, None)
                        record.INFO.pop(k, None)
                # for each sample, add new key of e.g m2_AD and set new key value as old key value
                for sample in self.samples:
                    for fmt in self.formats:
                        record.add_format(key=fmt, value=None)
                        record.call_for_sample[sample].data[fmt] = None
                        c, k = fmt.split('_', 1)
                        if c == caller:
                            record.call_for_sample[sample].data[fmt] = record.call_for_sample[sample].data.get(k, None)
                            # remove old entry of e.g AD
                            if k in record.FORMAT:
                                record.FORMAT.remove(k)
                                record.call_for_sample[sample].data.pop(k, None)
                if var_id not in records:
                    records[var_id] = record
                else:
                    # Uniquify for variants called by multiple callers
                    seen = records[var_id]
                    # add current record's filter to previously seen record's filter list
                    # typeError might occur if
                    for flt in record.FILTER:
                        try:
                            seen.add_filter(flt)
                        except TypeError:
                            pass
                    # for INFO and FORMAT ids, change values of seen var_ids to value
                        # from current record
                    for info in record.INFO:
                        c, k = info.split('_', 1)
                        if c == caller:
                            seen.INFO[info] = record.INFO[info]
                    for sample in self.samples:
                        for fmt in record.call_for_sample[sample].data:
                            c, k = fmt.split('_', 1)
                            if c == caller:
                                seen.call_for_sample[sample].data[fmt] = record.call_for_sample[sample].data[fmt]
                    records[var_id] = seen
            reader.close()
        return list(records.values())


class VcfSelecter:
    """
    In a merged VCF, select VCF fields of interest
    """
    def __init__(self, input_vcf, info_fields, format_fields, caller_priority, vcf_format="VCFv4.2"):
        self.reader = vcfpy.Reader.from_path(input_vcf)
        self.info_fields = info_fields
        self.format_fields = format_fields
        self.caller_priority = caller_priority
        self.samples = self.reader.header.samples
        self.header = vcfpy.Header(samples=self.samples)
        self.header.add_line(vcfpy.HeaderLine('fileformat', vcf_format))

    def select_headers(self):
        for contig in self.reader.header.get_lines('contig'):
            self.header.add_contig_line(vcfpy.OrderedDict([('ID', contig.id), ('length', contig.length)]))
        for flt in self.reader.header.get_lines('FILTER'):
            self.header.add_filter_line(vcfpy.OrderedDict([('ID', flt.id), ('Description', flt.description)]))
        for info_field in self.info_fields:
            for caller in self.caller_priority:
                info_id = '{}_{}'.format(caller, info_field)
                if info_id in self.reader.header.info_ids():
                    info = self.reader.header.get_info_field_info(info_id)
                    # AF in fb is Number = 1 unlike AF in m2 which is 'A'.
                    # this avoids vcfpy write errors
                    if info.id == 'AF' and caller == 'fb':
                        info.number = 'A'
                    self.header.add_info_line(vcfpy.OrderedDict([('ID', info.id.split('_', 1)[1]),
                                                                 ('Number', info.number),
                                                                 ('Type', info.type),
                                                                 ('Description', info.description.split(' ', 1)[1])]))
                    break
                else:
                    print('{} not found for {} in INFO column.'.format(info_field, caller))
        not_found = list(set(list(self.info_fields)) - set(self.header.info_ids()))
        if len(not_found) > 0:
            raise Exception(', '.join(not_found) + ' INFO field(s) not found in VCF')
        for format_field in self.format_fields:
            for caller in self.caller_priority:
                fmt_id = '{}_{}'.format(caller, format_field)
                if fmt_id in self.reader.header.format_ids():
                    fmt = self.reader.header.get_format_field_info(fmt_id)
                    self.header.add_format_line(vcfpy.OrderedDict([('ID', fmt.id.split('_', 1)[1]),
                                                                   ('Number', fmt.number),
                                                                   ('Type', fmt.type),
                                                                   ('Description', fmt.description.split(' ', 1)[1])]))
                    break
                else:
                    print('{} not found for {} in sample column.'.format(format_field, caller))
        not_found = list(set(list(self.format_fields)) - set(self.header.format_ids()))
        if len(not_found) > 0:
            raise Exception(', '.join(not_found) + ' FORMAT field(s) not found in VCF')
        return self.header

    def select_records(self):
        records = {}
        for record in self.reader:
            var_id = '{}:{}{}>{}'.format(record.CHROM, record.POS, record.REF, record.ALT)
            if var_id not in records:
                # get the first caller in the priority
                first_caller = None
                for filt in record.FILTER:
                    if filt in self.caller_priority:
                        first_caller = filt
                        break
                # get only info values from first caller
                for info in self.info_fields:
                    if first_caller:
                        caller_key = '{}_{}'.format(first_caller, info)
                    else:
                        raise Exception('No caller in given caller priority list in record: {}'.format(var_id))
                    if caller_key in record.INFO:
                        value = record.INFO.get(caller_key, None)
                        # if None or empty
                        if value:
                            record.INFO[info] = value
                # get values of info field of first or next priority caller
                # for info in self.info_fields:
                #     for caller in self.caller_priority:
                #         caller_key = '{}_{}'.format(caller, info)
                #         if caller_key in record.INFO:
                #             value = record.INFO.get(caller_key, None)
                #             if value:
                #                 record.INFO[info] = value
                #                 break

                # remove all info_fields not of interest
                for info in list(record.INFO):
                    if info not in self.info_fields:
                        record.INFO.pop(info, None)

                # get only sample values from first caller
                for sample in self.samples.names:
                    for fmt in self.format_fields:
                        caller_key = '{}_{}'.format(first_caller, fmt)
                        if caller_key in record.call_for_sample[sample].data:
                            value = record.call_for_sample[sample].data.get(caller_key, None)
                            # AF in fb is Number = 1 unlike AF in m2 which is 'A'. This avoids vcfpy write errors
                            if caller_key == 'fb_AF':
                                value = [value]
                            if value:
                                record.call_for_sample[sample].data[fmt] = value
                                record.FORMAT.append(fmt)
                # remove all info_fields not of interest
                for call in record.calls:
                    for fmt in list(call.data):
                        if fmt not in self.format_fields:
                            call.data.pop(fmt, None)
                            if fmt in record.FORMAT:
                                record.FORMAT.remove(fmt)

            records[var_id] = record
        return list(records.values())