import unittest
from unittest.mock import MagicMock, patch

from resume_parser_script import TextFilter
# import nltk

class TestTextFilter(unittest.TestCase):
    def test_clean_text(self):
        tf = TextFilter("Café! Déjà vu? Test 123.")
        cleaned = tf.clean_text()
        self.assertEqual(cleaned, 'Cafe Deja vu Test 123')


    def test_extract_keywords(self):
        ek = TextFilter("To be honest, today was a good day.")
        extract_filter = ek.extract_keywords()
        expected_keyword = ['honest', 'today', 'good', 'day']
        self.assertEqual(extract_filter, expected_keyword)

    @patch('resume_parser_script.psycopg2.connect')
    @patch('resume_parser_script.os.getenv') # decorators that mock the psycopg2.connect function and the os.getenv call
    # inside the resume_parser_script module.

    # *order is reversed when passed into the function*
    def test_init_database(self, mock_getenv, mock_connect):  # the function receives the mocked versions of "os.getenv"
        # and "psycopg2.connect", respectively

        mock_conn = MagicMock()  # simulates a database connection
        mock_connect.return_value = mock_conn  # telling mock_connect() to return mock_conn

        mock_getenv.return_value = "fake_password"  # mock get_env() will return 'fake password' when called with a key
        result = TextFilter.init_database() # here we call the actual function

        mock_getenv.assert_called_with("SECRET_PASSWORD") # check that the code tired to fetch the "SECRET_PASSWORD"
        # from the environment

        mock_connect.assert_called_with(
            dbname = 'postgres',
            user = 'matthewyakubu',
            password = 'fake_password',
            host = 'localhost',
            port = '5432'
        )  # checks that the psycopg2.connect call used the expected parameters.

        self.assertEqual(result, mock_conn) # check that the method returns the mock connection

if __name__ == '__main__':
    unittest.main()

