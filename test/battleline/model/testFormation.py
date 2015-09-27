import unittest
from battleline.model.Formation import Formation, FormationInvalidError
class TestFormation(unittest.TestCase):

    def test_formation_with_less_than_three_cards_is_considered_invalid(self):
        self.assertRaisesRegexp(FormationInvalidError, "Formation must have 3 cards", Formation, [(1, "R"), (2, "Y")])

    def test_formation_with_more_than_three_cards_is_considered_invalid(self):
        self.assertRaisesRegexp(FormationInvalidError, "Formation must have 3 cards", Formation, [(1, "R"), (2, "Y"), (3, "R"), (5, "G")])

    def test_can_get_formation_numbers_in_sorted_fashion(self):
        formation = Formation([(1, "R"), (3, "Y"), (2, "R")])
        self.assertEquals((1,2,3), formation.get_numbers())

        formation = Formation([(10, "R"), (9, "Y"), (8, "R")])
        self.assertEquals((8,9,10), formation.get_numbers())

    def test_can_get_formation_colors_in_sorted_fashion(self):
        formation = Formation([(1, "R"), (3, "Y"), (2, "R")])
        self.assertEquals(("R", "Y", "R"), formation.get_colors())

        formation = Formation([(10, "G"), (9, "Y"), (8, "R")])
        self.assertEquals(("G", "Y", "R"), formation.get_colors())

    def test_can_get_max_number(self):
        formation = Formation([(1, "R"), (3, "Y"), (2, "R")])
        self.assertEquals(3, formation.get_max_number())

        formation = Formation([(10, "G"), (9, "Y"), (8, "R")])
        self.assertEquals(10, formation.get_max_number())


    def test_can_check_for_wedge(self):
        formation = Formation([(1, "R"), (2, "R"), (3, "R")])
        self.assertTrue(formation.is_wedge())

        formation = Formation([(10, "G"), (9, "G"), (8, "G")])
        self.assertTrue(formation.is_wedge())

    def test_missing_number_is_not_wedge(self):
        formation = Formation([(1, "R"), (4, "R"), (3, "R")])
        self.assertFalse(formation.is_wedge())

    def test_missing_color_is_not_wedge(self):
        formation = Formation([(1, "R"), (2, "R"), (3, "G")])
        self.assertFalse(formation.is_wedge())

    def test_can_check_for_phalanx(self):
        formation = Formation([(1, "R"), (1, "G"), (1, "Y")])
        self.assertTrue(formation.is_phalanx())

        formation = Formation([(10, "Y"), (10, "G"), (10, "B")])
        self.assertTrue(formation.is_phalanx())

    def test_two_of_a_kind_is_not_a_phalanx(self):
        formation = Formation([(1, "R"), (1, "G"), (2, "R")])
        self.assertFalse(formation.is_phalanx())

    def test_can_check_for_battalion(self):
        formation = Formation([(1, "Y"), (2, "Y"), (3, "Y")])
        self.assertTrue(formation.is_battalion())

        formation = Formation([(10, "G"), (9, "G"), (10, "G")])
        self.assertTrue(formation.is_battalion())

    def test_two_of_a_color_is_not_a_battalion(self):
        formation = Formation([(1, "R"), (3, "G"), (2, "R")])
        self.assertFalse(formation.is_battalion())

    def test_can_check_for_skirmish(self):
        formation = Formation([(1, "Y"), (2, "B"), (3, "Y")])
        self.assertTrue(formation.is_skirmish())

        formation = Formation([(10, "G"), (9, "B"), (8, "G")])
        self.assertTrue(formation.is_skirmish())

    def test_non_straight_is_not_a_skirmish(self):
        formation = Formation([(1, "R"), (4, "G"), (2, "R")])
        self.assertFalse(formation.is_skirmish())

    def test_is_host(self):
        formation = Formation([(1, "R"), (5, "G"), (5, "R")])
        self.assertTrue(formation.is_host())

    def test_formation_equality_with_self(self):
        self.assertTrue(Formation([(1, "R"), (2, "R"), (3, "R")]).is_equivalent_in_strength( Formation([(1, "R"), (2, "R"), (3, "R")])))

    def test_formation_equality_with_wedge_and_host(self):
        self.assertFalse(Formation([(1, "R"), (2, "R"), (3, "R")]).is_equivalent_in_strength( Formation([(1, "B"), (2, "B"), (4, "G")])))
        self.assertFalse(Formation([(5, "R"), (1, "R"), (3, "Y")]).is_equivalent_in_strength( Formation([(2, "B"), (3, "B"), (4, "B")])))

    def test_formation_equality_with_two_wedges(self):
        self.assertTrue(Formation([(1, "R"), (2, "R"), (3, "R")]).is_equivalent_in_strength( Formation([(1, "G"), (2, "G"), (3, "G")])))

    def test_formation_equality_with_wedge_and_battalion(self):
        self.assertFalse(Formation([(4, "R"), (2, "R"), (3, "R")]).is_equivalent_in_strength( Formation([(5, "G"), (1, "G"), (3, "G")])))

    def test_formation_equality_with_wedge_and_skirmish(self):
        self.assertFalse(Formation([(1, "R"), (2, "R"), (3, "R")]).is_equivalent_in_strength( Formation([(1, "G"), (2, "G"), (3, "B")])))

    def test_formation_equality_with_two_phalanxes(self):
        self.assertTrue(Formation([(1, "R"), (1, "G"), (1, "Y")]).is_equivalent_in_strength( Formation([(1, "P"), (1, "B"), (1, "O")])))
        self.assertFalse(Formation([(1, "R"), (1, "G"), (1, "Y")]).is_equivalent_in_strength( Formation([(2, "P"), (2, "B"), (2, "O")])))

    def test_formation_equality_with_two_battalions(self):
        self.assertTrue(Formation([(3, "R"), (2, "R"), (5, "R")]).is_equivalent_in_strength( Formation([(5, "B"), (2, "B"), (3, "B")])))
        self.assertFalse(Formation([(6, "R"), (2, "R"), (3, "R")]).is_equivalent_in_strength( Formation([(5, "B"), (2, "B"), (3, "B")])))

    def test_formation_equality_with_two_skirmishes(self):
        self.assertTrue(Formation([(1, "R"), (2, "R"), (3, "Y")]).is_equivalent_in_strength( Formation([(1, "B"), (2, "B"), (3, "G")])))
        self.assertFalse(Formation([(1, "R"), (2, "R"), (3, "Y")]).is_equivalent_in_strength( Formation([(4, "B"), (2, "B"), (3, "G")])))

    def test_formation_equality_with_two_hosts(self):
        self.assertTrue(Formation([(1, "R"), (4, "Y"), (3, "R")]).is_equivalent_in_strength( Formation([(1, "G"), (4, "G"), (3, "B")])))
        self.assertFalse(Formation([(1, "R"), (2, "Y"), (3, "R")]).is_equivalent_in_strength( Formation([(4, "G"), (2, "G"), (3, "B")])))

    def test_greater_than_check_two_wedges(self):
        self.assertTrue(Formation([(4, "R"), (2, "R"), (3, "R")]).is_greater_strength_than(Formation([(1, "R"), (2, "R"), (3, "R")])))
        self.assertFalse(Formation([(1, "R"), (2, "R"), (3, "R")]).is_greater_strength_than(Formation([(1, "R"), (2, "R"), (3, "R")])))

    def test_greater_than_check_wedge_and_phalanx(self):
        self.assertTrue(Formation([(1, "R"), (2, "R"), (3, "R")]).is_greater_strength_than(Formation([(2, "R"), (2, "G"), (2, "B")])))


    def test_greater_than_check_two_phalanxes(self):
        self.assertTrue(Formation([(2, "Y"), (2, "R"), (2, "B")]).is_greater_strength_than(Formation([(1, "Y"), (1, "R"), (1, "B")])))
        self.assertFalse(Formation([(2, "Y"), (2, "R"), (2, "B")]).is_greater_strength_than(Formation([(2, "P"), (2, "G"), (2, "O")])))

    def test_greater_than_check_phalanx_and_battalion(self):
        self.assertTrue(Formation([(3, "Y"), (3, "R"), (3, "B")]).is_greater_strength_than(Formation([(1, "G"), (3, "G"), (5, "G")])))
