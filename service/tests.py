import unittest

from service import database


class TestDatabase(unittest.TestCase):
    def test_db_ruian(self):
        info = database.db_info("ruian")
        self.assertIsNotNone(info, "Musí existovat připojení k serveru a databázi")
        nam = info.get("dbname")
        self.assertEqual(nam, "ruian", "Databáze musí být 'ruian'")

    def test_db_povodi(self):
        info = database.db_info("povodi")
        self.assertIsNotNone(info, "Musí existovat připojení k serveru a databázi")
        nam = info.get("dbname")
        self.assertEqual(nam, "povodi", "Databáze musí být 'povodi'")

    def test_ruian_version(self):
        dv = database.get_ruian_version()
        self.assertIsNotNone(dv, "Musí existovat datum RUIAN")
        print(dv)

    def test_get_table_names(self):
        tn = database.get_table_names("ruian")
        self.assertIsNotNone(tn, "Musí existovat seznam tabulek databáze 'ruian'")
        print(tn)
        tn = database.get_table_names("povodi")
        self.assertIsNotNone(tn, "Musí existovat seznam tabulek databáze 'povodi'")
        print(tn)

    def test_get_table_size(self):
        cn = database.get_table_size("ruian", "adresnimista")
        self.assertIsNotNone(cn, "Musí existovat výsledek")
        self.assertGreaterEqual(cn, 0, "Výsledek musí být >= 0")
        print("ruian", "adresnimista", cn)


"""        
    def test_get_tables(self):
        tab = database.get_tables("ruian")
        self.assertIsNotNone(tab, "Musí existovat nějaké tabulky databáze 'ruian'")
        print(tab)
"""

if __name__ == '__main__':
    unittest.main()
