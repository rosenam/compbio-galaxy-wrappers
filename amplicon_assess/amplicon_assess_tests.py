from collections import OrderedDict
import amplicon_assess
import pysam
import unittest
import vcfpy

class QiagenPrimersTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        filename = "test/bed_test.bed"
        cls.primers = amplicon_assess.QiagenPrimers(filename)

    def test_primer_regions(self):
        exp = {('3', 171087373): 0, ('3', 174814819): 0, ('3', 178545893): 0, ('3', 178916663): 0,
               ('3', 178916730): 1, ('3', 178916944): 1, ('3', 178917043): 1, ('3', 178917535): 0,
               ('3', 178917615): 1, ('3', 178917743): 1, ('3', 178919033): 0, ('3', 178919195): 0,
               ('3', 178919330): 1, ('3', 178921395): 0, ('3', 178921441): 0, ('3', 178921464): 1,
               ('3', 178922229): 0, ('3', 178922438): 1, ('3', 178927523): 1, ('3', 178927555): 1,
               ('3', 178927993): 0, ('3', 178928099): 1, ('3', 178928222): 0, ('3', 178928357): 1,
               ('3', 178935987): 0, ('3', 178936108): 1, ('3', 178936141): 1, ('3', 178936227): 1,
               ('3', 178936921): 0, ('3', 178937417): 0, ('3', 178937493): 1, ('3', 178937691): 0,
               ('3', 178937986): 1, ('3', 178938898): 1, ('3', 178938987): 1, ('3', 178941858): 0,
               ('3', 178941997): 1, ('3', 178942464): 0, ('3', 178942620): 1, ('3', 178943883): 1,
               ('3', 178947015): 0, ('3', 178947095): 0, ('3', 178947741): 0, ('3', 178947782): 0,
               ('3', 178948072): 0, ('3', 178948150): 1, ('3', 178951823): 0, ('3', 178951840): 0,
               ('3', 178951922): 0, ('3', 178952007): 0, ('3', 178952122): 1, ('3', 178952219): 1,
               ('5', 150311841): 1, ('5', 154065194): 0, ('5', 156679444): 0, ('5', 159505153): 0,
               ('12', 25243006): 0, ('12', 25362671): 0, ('12', 25362907): 1, ('12', 25368332): 0,
               ('12', 25368554): 1, ('12', 25378487): 0, ('12', 25378536): 0, ('12', 25378618): 1,
               ('12', 25378767): 1, ('12', 25378781): 1, ('12', 25380241): 0, ('12', 25380289): 1,
               ('12', 25380311): 1, ('12', 25380366): 1, ('12', 25380389): 1, ('12', 25398134): 0,
               ('12', 25398195): 0, ('12', 25398272): 1, ('12', 25398402): 1, ('X', 20146513): 1,
               ('X', 20148603): 0, ('X', 20148759): 1, ('X', 20150231): 0, ('X', 20150269): 0,
               ('X', 20151996): 0, ('X', 20153972): 1, ('X', 20154042): 1, ('X', 20156630): 0,
               ('X', 20156746): 1, ('X', 20159664): 0}
        self.assertEqual(exp, self.primers.my_primers)

    def test_parse_bed(self):
        exp = OrderedDict(
            [(('3', 171087408, 171087622), 0), (('3', 174814853, 174815068), 0), (('3', 178545927, 178546142), 0),
             (('3', 178916701, 178916912), 0), (('3', 178916481, 178916700), 1), (('3', 178916695, 178916911), 1),
             (('3', 178916794, 178917004), 1), (('3', 178917571, 178917784), 0), (('3', 178917366, 178917581), 1),
             (('3', 178917494, 178917704), 1), (('3', 178919069, 178919282), 0), (('3', 178919228, 178919444), 0),
             (('3', 178919081, 178919291), 1), (('3', 178921431, 178921644), 0), (('3', 178921475, 178921690), 0),
             (('3', 178921215, 178921436), 1), (('3', 178922269, 178922478), 0), (('3', 178922189, 178922399), 1),
             (('3', 178927274, 178927482), 1), (('3', 178927306, 178927514), 1), (('3', 178928034, 178928242), 0),
             (('3', 178927850, 178928063), 1), (('3', 178928253, 178928471), 0), (('3', 178928108, 178928329), 1),
             (('3', 178936030, 178936236), 0), (('3', 178935859, 178936076), 1), (('3', 178935892, 178936105), 1),
             (('3', 178935978, 178936186), 1), (('3', 178936953, 178937170), 0), (('3', 178937449, 178937666), 0),
             (('3', 178937244, 178937457), 1), (('3', 178937720, 178937940), 0), (('3', 178937737, 178937945), 1),
             (('3', 178938649, 178938868), 1), (('3', 178938738, 178938954), 1), (('3', 178941899, 178942107), 0),
             (('3', 178941748, 178941966), 1), (('3', 178942504, 178942713), 0), (('3', 178942371, 178942585), 1),
             (('3', 178943634, 178943845), 1), (('3', 178947054, 178947264), 0), (('3', 178947123, 178947344), 0),
             (('3', 178947781, 178947990), 0), (('3', 178947818, 178948031), 0), (('3', 178948100, 178948321), 0),
             (('3', 178947901, 178948117), 1), (('3', 178951858, 178952072), 0), (('3', 178951876, 178952089), 0),
             (('3', 178951960, 178952171), 0), (('3', 178952042, 178952256), 0), (('3', 178951873, 178952092), 1),
             (('3', 178951970, 178952189), 1), (('5', 150311592, 150311805), 1), (('5', 154065225, 154065443), 0),
             (('5', 156679479, 156679693), 0), (('5', 159505187, 159505402), 0), (('12', 25243042, 25243255), 0),
             (('12', 25362712, 25362920), 0), (('12', 25362658, 25362870), 1), (('12', 25368369, 25368581), 0),
             (('12', 25368305, 25368518), 1), (('12', 25378527, 25378736), 0), (('12', 25378571, 25378785), 0),
             (('12', 25378369, 25378587), 1), (('12', 25378518, 25378726), 1), (('12', 25378532, 25378741), 1),
             (('12', 25380271, 25380490), 0), (('12', 25380040, 25380262), 1), (('12', 25380062, 25380280), 1),
             (('12', 25380117, 25380335), 1), (('12', 25380140, 25380354), 1), (('12', 25398170, 25398383), 0),
             (('12', 25398234, 25398444), 0), (('12', 25398023, 25398243), 1), (('12', 25398153, 25398361), 1),
             (('X', 20146264, 20146477), 1), (('X', 20148639, 20148852), 0), (('X', 20148510, 20148723), 1),
             (('X', 20150266, 20150480), 0), (('X', 20150308, 20150518), 0), (('X', 20152030, 20152245), 0),
             (('X', 20153723, 20153943), 1), (('X', 20153793, 20154006), 1), (('X', 20156666, 20156879), 0),
             (('X', 20156497, 20156716), 1), (('X', 20159687, 20159913), 0)])
        self.assertEqual(exp, self.primers.my_roi)

    def test_get_pcoords(self):
        start = 200
        stop = 400
        strand = 0
        exp = 151
        self.assertEqual(exp, self.primers._get_pcoords(start, stop, strand))
        strand = 1
        exp = self.primers._get_pcoords(start, stop, strand)
        self.assertEqual(exp, self.primers._get_pcoords(start, stop, strand))
        strand = 2
        self.assertRaises(ValueError, self.primers._get_pcoords, start, stop, strand)


class VrntMetricsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.samfile = pysam.AlignmentFile("test/umi_dedup.bam", "rb")
        cls.primers = amplicon_assess.QiagenPrimers("test/bed_test.bed").my_primers
        cls.reader = vcfpy.Reader.from_path("test/vcf_test.vcf.gz")
        # print(self.primers)

    def setUp(self):
        vrnt = ("3", 178952085)
        self.metrics = amplicon_assess.VrntMetrics(self.samfile, vrnt, self.primers)

    def test_check_all_primers(self, dist=5):
        exp_primer = 178952219
        coord = exp_primer - dist + 1
        bad_coord = exp_primer - dist - 1
        self.assertEqual(exp_primer, self.metrics._check_all_primers(coord, dist))
        self.assertEqual(None, self.metrics._check_all_primers(bad_coord, dist))

    def test_add_bases(self):
        old = {'A': [0, 1]}
        new = {'A': [1, 0], 'T': [5, 6]}
        expected = {'A': [1, 1], 'T': [5, 6]}
        self.assertEqual(expected, self.metrics._add_bases(old, new))

    # def test_collect_basecalls_region(self):
    #     exp_raw_metrics = {(2, 178951876): {'T': 2527, 'A': 2, 'G': 7, 'C': 3}, (2, 178951898): {'T': 1},
    #                        (2, 178951902): {'T': 3}, (2, 178951904): {'T': 1}, (2, 178951909): {'T': 1},
    #                        (2, 178951913): {'T': 1}, (2, 178951918): {'T': 18, 'C': 1}, (2, 178951919): {'T': 1},
    #                        (2, 178951921): {'T': 1}, (2, 178951922): {'T': 10}, (2, 178951923): {'T': 2, 'C': 1},
    #                        (2, 178951926): {'T': 2}, (2, 178951927): {'T': 1}, (2, 178951928): {'T': 1},
    #                        (2, 178951929): {'T': 1}, (2, 178951933): {'T': 1}, (2, 178951934): {'T': 1},
    #                        (2, 178951938): {'T': 1}, (2, 178951939): {'T': 1}, (2, 178951941): {'T': 2},
    #                        (2, 178951943): {'T': 1}, (2, 178951945): {'T': 1}, (2, 178951946): {'T': 2},
    #                        (2, 178951948): {'T': 1}, (2, 178951951): {'T': 1}, (2, 178951952): {'T': 1},
    #                        (2, 178951953): {'T': 1}, (2, 178951955): {'T': 1}, (2, 178951957): {'T': 1},
    #                        (2, 178951959): {'T': 1}, (2, 178951960): {'T': 3}, (2, 178951961): {'T': 1},
    #                        (2, 178951963): {'T': 2}, (2, 178951964): {'T': 2}, (2, 178951965): {'T': 3},
    #                        (2, 178951966): {'T': 3}, (2, 178951969): {'T': 3}, (2, 178951970): {'T': 1},
    #                        (2, 178951973): {'T': 1}, (2, 178951974): {'T': 7}, (2, 178951975): {'T': 4},
    #                        (2, 178951976): {'T': 4}, (2, 178951981): {'T': 2}, (2, 178951982): {'T': 1},
    #                        (2, 178951983): {'T': 3}, (2, 178951984): {'T': 2}, (2, 178951985): {'T': 6},
    #                        (2, 178951986): {'T': 1}, (2, 178951988): {'T': 3}, (2, 178951989): {'T': 4},
    #                        (2, 178951990): {'T': 1}, (2, 178951992): {'T': 5}, (2, 178951993): {'T': 3},
    #                        (2, 178951994): {'T': 2}, (2, 178951995): {'T': 1}, (2, 178951996): {'T': 2},
    #                        (2, 178951997): {'T': 3}, (2, 178951999): {'T': 2}, (2, 178952001): {'T': 5},
    #                        (2, 178952002): {'T': 316}, (2, 178952003): {'T': 5}, (2, 178952004): {'T': 8},
    #                        (2, 178952006): {'T': 3}, (2, 178952007): {'T': 262}, (2, 178952008): {'T': 23},
    #                        (2, 178952009): {'T': 5}, (2, 178952010): {'T': 3}, (2, 178952011): {'T': 6},
    #                        (2, 178952012): {'T': 10}, (2, 178952013): {'T': 4}, (2, 178952014): {'T': 2},
    #                        (2, 178952015): {'T': 1}, (2, 178952016): {'T': 2}, (2, 178952018): {'T': 7},
    #                        (2, 178952019): {'T': 7}, (2, 178952020): {'T': 3}, (2, 178952023): {'T': 2},
    #                        (2, 178952024): {'T': 3}, (2, 178952025): {'T': 62, 'C': 1}, (2, 178952026): {'T': 1},
    #                        (2, 178952028): {'T': 6}, (2, 178952029): {'T': 5}, (2, 178952030): {'T': 6},
    #                        (2, 178952031): {'T': 4}, (2, 178952032): {'T': 2}, (2, 178952033): {'T': 9},
    #                        (2, 178952034): {'T': 2}, (2, 178952035): {'A': 1, 'T': 1}, (2, 178952036): {'T': 8},
    #                        (2, 178952037): {'T': 7}, (2, 178952038): {'T': 5}, (2, 178952040): {'T': 7},
    #                        (2, 178952041): {'T': 4}, (2, 178952042): {'T': 6}, (2, 178952043): {'T': 5},
    #                        (2, 178952044): {'T': 6}, (2, 178952045): {'T': 4}, (2, 178952046): {'T': 6},
    #                        (2, 178952047): {'G': 1, 'T': 6}, (2, 178952048): {'T': 13}, (2, 178952049): {'T': 2},
    #                        (2, 178952050): {'T': 2}, (2, 178952051): {'T': 2}, (2, 178952052): {'T': 16},
    #                        (2, 178952053): {'T': 6}, (2, 178952054): {'T': 5}, (2, 178952055): {'T': 1},
    #                        (2, 178952056): {'T': 1}, (2, 178952057): {'T': 8}, (2, 178952058): {'T': 4},
    #                        (2, 178952059): {'T': 3}, (2, 178952060): {'T': 2}, (2, 178952061): {'T': 12},
    #                        (2, 178952062): {'T': 6}, (2, 178952063): {'T': 2}, (2, 178952064): {'T': 12},
    #                        (2, 178952065): {'T': 5}, (2, 178952066): {'T': 2}, (2, 178952067): {'T': 1},
    #                        (2, 178952068): {'T': 9}, (2, 178952069): {'T': 6}, (2, 178952070): {'T': 4},
    #                        (2, 178952071): {'T': 2}, (2, 178952072): {'T': 4}, (2, 178952073): {'T': 8},
    #                        (2, 178952076): {'T': 1}, (2, 178952077): {'T': 6}, (2, 178952079): {'T': 2},
    #                        (2, 178952080): {'T': 3, 'C': 1}, (2, 178952081): {'T': 2}, (2, 178952082): {'T': 4},
    #                        (2, 178952084): {'T': 3}}
    #     exp_end_coords = {(2, 178951876): [178952122, 178952122], (2, 178951898): [178952122], (2, 178951902): [178952108, 178952122, 178952122], (2, 178951904): [178952122], (2, 178951909): [178952122], (2, 178951913): [178952122], (2, 178951918): [178952122, 178952122], (2, 178951919): [178952122], (2, 178951921): [178952122], (2, 178951922): [178952091, 178952095, 178952096, 178952099, 178952107, 178952109, 178952122, 178952122, 178952125, 178952160], (2, 178951923): [178952122, 178952122, 178952102], (2, 178951926): [178952122, 178952122], (2, 178951927): [178952122], (2, 178951928): [178952122], (2, 178951929): [178952122], (2, 178951933): [178952122], (2, 178951934): [178952122], (2, 178951938): [178952122], (2, 178951939): [178952122], (2, 178951941): [178952122, 178952122], (2, 178951943): [178952122], (2, 178951945): [178952122], (2, 178951946): [178952122, 178952122], (2, 178951948): [178952122], (2, 178951951): [178952122], (2, 178951952): [178952122], (2, 178951953): [178952122], (2, 178951955): [178952122], (2, 178951957): [178952122], (2, 178951959): [178952122], (2, 178951960): [178952122, 178952122, 178952122], (2, 178951961): [178952122], (2, 178951963): [178952122, 178952122], (2, 178951964): [178952122, 178952122], (2, 178951965): [178952122, 178952122, 178952122], (2, 178951966): [178952122, 178952122, 178952122], (2, 178951969): [178952122, 178952122, 178952122], (2, 178951970): [178952122], (2, 178951973): [178952122], (2, 178951974): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178951975): [178952122, 178952122, 178952122, 178952121], (2, 178951976): [178952122, 178952122, 178952122, 178952122], (2, 178951981): [178952122, 178952122], (2, 178951982): [178952122], (2, 178951983): [178952122, 178952122, 178952122], (2, 178951984): [178952122, 178952122], (2, 178951985): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178951986): [178952122], (2, 178951988): [178952122, 178952122, 178952122], (2, 178951989): [178952122, 178952122, 178952122, 178952122], (2, 178951990): [178952122], (2, 178951992): [178952122, 178952122, 178952122, 178952122, 178952122], (2, 178951993): [178952122, 178952122, 178952122], (2, 178951994): [178952122, 178952122], (2, 178951995): [178952122], (2, 178951996): [178952122, 178952122], (2, 178951997): [178952122, 178952122, 178952122], (2, 178951999): [178952122, 178952122], (2, 178952001): [178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952002): [178952122], (2, 178952003): [178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952004): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952006): [178952122, 178952122, 178952122], (2, 178952007): [178952120, 178952122, 178952087, 178952088, 178952088, 178952088, 178952088, 178952089, 178952089, 178952090, 178952090, 178952090, 178952091, 178952091, 178952091, 178952092, 178952094, 178952094, 178952094, 178952094, 178952094, 178952094, 178952094, 178952095, 178952095, 178952096, 178952096, 178952096, 178952096, 178952096, 178952096, 178952096, 178952096, 178952096, 178952096, 178952096, 178952097, 178952098, 178952098, 178952099, 178952099, 178952099, 178952099, 178952099, 178952099, 178952099, 178952099, 178952099, 178952099, 178952099, 178952099, 178952099, 178952099, 178952100, 178952100, 178952100, 178952100, 178952100, 178952100, 178952100, 178952101, 178952102, 178952102, 178952102, 178952102, 178952102, 178952102, 178952102, 178952102, 178952103, 178952103, 178952103, 178952104, 178952104, 178952104, 178952104, 178952105, 178952106, 178952107, 178952108, 178952108, 178952108, 178952108, 178952108, 178952108, 178952109, 178952109, 178952109, 178952107, 178952109, 178952109, 178952109, 178952109, 178952109, 178952109, 178952109, 178952109, 178952110, 178952110, 178952110, 178952110, 178952110, 178952110, 178952111, 178952111, 178952111, 178952111, 178952111, 178952111, 178952111, 178952112, 178952112, 178952112, 178952112, 178952112, 178952112, 178952112, 178952112, 178952112, 178952114, 178952115, 178952116, 178952117, 178952117, 178952117, 178952119, 178952119, 178952119, 178952120, 178952120, 178952120, 178952121, 178952121, 178952121, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952123, 178952124, 178952124, 178952124, 178952124, 178952124, 178952124, 178952124, 178952125, 178952125, 178952126, 178952126, 178952126, 178952126, 178952126, 178952126, 178952126, 178952127, 178952127, 178952129, 178952130, 178952132, 178952132, 178952133, 178952133, 178952134, 178952134, 178952134, 178952134, 178952134, 178952134, 178952134, 178952134, 178952134, 178952134, 178952134, 178952136, 178952137, 178952137, 178952138, 178952138, 178952138, 178952139, 178952139, 178952140, 178952141, 178952141, 178952144, 178952144, 178952144, 178952144, 178952147, 178952148, 178952148, 178952148, 178952148, 178952152, 178952152, 178952153, 178952153, 178952153, 178952154, 178952155, 178952155, 178952155, 178952158, 178952158, 178952160, 178952160, 178952162, 178952164, 178952165, 178952168, 178952169, 178952169, 178952170, 178952170, 178952170, 178952173, 178952173, 178952173, 178952173, 178952173, 178952173, 178952182, 178952183, 178952184, 178952185, 178952185, 178952185, 178952186, 178952186, 178952190, 178952190, 178952191, 178952191, 178952191, 178952191, 178952191, 178952191, 178952194, 178952196, 178952197, 178952202, 178952203, 178952203, 178952204, 178952212, 178952219, 178952225, 178952234, 178952236, 178952237, 178952243, 178952245, 178952271], (2, 178952008): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952009): [178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952010): [178952122, 178952122, 178952122], (2, 178952011): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952012): [178952122, 178952122, 178952122, 178952122, 178952122, 178952121, 178952122, 178952122, 178952122, 178952122], (2, 178952013): [178952122, 178952122, 178952122, 178952122], (2, 178952014): [178952122, 178952164], (2, 178952015): [178952122], (2, 178952016): [178952122, 178952122], (2, 178952018): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952019): [178952122, 178952122, 178952122, 178952122, 178952121, 178952122, 178952122], (2, 178952020): [178952122, 178952122, 178952122], (2, 178952023): [178952122, 178952122], (2, 178952024): [178952122, 178952122, 178952122], (2, 178952025): [178952122, 178952122, 178952122, 178952122, 178952122, 178952219, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952026): [178952122], (2, 178952028): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952029): [178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952030): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952031): [178952122, 178952122, 178952122, 178952122], (2, 178952032): [178952122, 178952122], (2, 178952033): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952034): [178952122, 178952122], (2, 178952035): [178952122, 178952122], (2, 178952036): [178952122, 178952122, 178952122, 178952122, 178952122, 178952219, 178952122, 178952122], (2, 178952037): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952038): [178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952040): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952041): [178952122, 178952122, 178952122, 178952122], (2, 178952042): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952043): [178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952044): [178952122, 178952219, 178952122, 178952122, 178952122, 178952122], (2, 178952045): [178952122, 178952122, 178952122, 178952122], (2, 178952046): [178952219, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952047): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952048): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952049): [178952122, 178952122], (2, 178952050): [178952122, 178952122], (2, 178952051): [178952122, 178952122], (2, 178952052): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952053): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952054): [178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952055): [178952122], (2, 178952056): [178952122], (2, 178952057): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952058): [178952122, 178952122, 178952122, 178952122], (2, 178952059): [178952122, 178952122, 178952122], (2, 178952060): [178952122, 178952122], (2, 178952061): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952219], (2, 178952062): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952063): [178952122, 178952122], (2, 178952064): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952065): [178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952066): [178952122, 178952219], (2, 178952067): [178952122], (2, 178952068): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952069): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952070): [178952122, 178952122, 178952122, 178952219], (2, 178952071): [178952122, 178952122], (2, 178952072): [178952122, 178952122, 178952122, 178952122], (2, 178952073): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122, 178952219, 178952122], (2, 178952076): [178952122], (2, 178952077): [178952122, 178952122, 178952122, 178952122, 178952122, 178952122], (2, 178952079): [178952122, 178952122], (2, 178952080): [178952122, 178952122, 178952219, 178952122], (2, 178952081): [178952122, 178952122], (2, 178952082): [178952122, 178952122, 178952122, 178952122], (2, 178952084): [178952122, 178952122, 178952122]}
    #     self.assertEqual(exp_raw_metrics, self.metrics.raw_metrics)
    #     self.assertEqual(exp_end_coords, self.metrics.end_coords)

    @classmethod
    def tearDownClass(cls):
        cls.samfile.close()
        cls.reader.close()

if __name__ == '__main__':
    unittest.main()