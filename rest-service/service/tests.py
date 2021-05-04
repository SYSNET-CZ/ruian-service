import unittest

from database import DATABASE_NAME_RUIAN, DATABASE_NAME_POVODI
from service import database
from service import query


class TestDatabase(unittest.TestCase):
    def test_db_ruian(self):
        info = database.db_info(DATABASE_NAME_RUIAN)
        self.assertIsNotNone(info, "Musí existovat připojení k serveru a databázi")
        nam = info.get("dbname")
        self.assertEqual(nam, DATABASE_NAME_RUIAN, "Databáze musí být '{}'".format(DATABASE_NAME_RUIAN))

    def test_db_povodi(self):
        info = database.db_info(DATABASE_NAME_POVODI)
        self.assertIsNotNone(info, "Musí existovat připojení k serveru a databázi")
        nam = info.get("dbname")
        self.assertEqual(nam, DATABASE_NAME_POVODI, "Databáze musí být '{}'".format(DATABASE_NAME_POVODI))

    def test_ruian_version(self):
        dv = database.get_ruian_version()
        self.assertIsNotNone(dv, "Musí existovat datum RUIAN")
        print(dv)

    def test_get_table_names(self):
        tn = database.get_table_names(DATABASE_NAME_RUIAN)
        self.assertIsNotNone(tn, "Musí existovat seznam tabulek databáze '{}'".format(DATABASE_NAME_RUIAN))
        print(tn)
        tn = database.get_table_names(DATABASE_NAME_POVODI)
        self.assertIsNotNone(tn, "Musí existovat seznam tabulek databáze '{}'".format(DATABASE_NAME_POVODI))
        print(tn)

    def test_get_table_size(self):
        cn = database.get_table_size(DATABASE_NAME_RUIAN, "adresnimista")
        self.assertIsNotNone(cn, "Musí existovat výsledek")
        self.assertGreaterEqual(cn, 0, "Výsledek musí být >= 0")
        print("ruian", "adresnimista", cn)


"""        
    def test_get_tables(self):
        tab = database.get_tables(DATABASE_NAME_RUIAN)
        self.assertIsNotNone(tab, "Musí existovat nějaké tabulky databáze 'ruian'")
        print(tab)
"""


class TestQuery(unittest.TestCase):
    def test_find_address(self):
        ap = 78395364
        result = query._find_address(ap)
        self.assertIsNotNone(result, "Musí nalézt místo")
        self.assertEqual(result.house_number, "105", "Číslo domu musí být 105")
        print(ap, result.locality, result.house_number)


if __name__ == '__main__':
    unittest.main()
