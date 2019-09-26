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


if __name__ == '__main__':
    unittest.main()
