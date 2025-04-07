import unittest
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



if __name__ == '__main__':
    unittest.main()

