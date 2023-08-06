from click.testing import CliRunner
import unittest
from fancywallet import PhilSfancywallet 

#adding a comment to test the commit.
class FancyWalletGetPriceTests(unittest.TestCase):

    def test_get_price_tsla_lower(self):
        runner = CliRunner()
        result = runner.invoke(PhilSfancywallet, ['get', 'price', 'tsla'])
        self.assertEqual(result.exit_code, 0)

    def test_get_price_tsla_upper(self):
        runner = CliRunner()
        result = runner.invoke(PhilSfancywallet, ['get', 'price', 'TSLA'])
        self.assertEqual(result.exit_code, 0)
        
    def test_get_price_unknown(self):
        company = 'unknown'
        runner = CliRunner()
        result = runner.invoke(PhilSfancywallet, ['get', 'price', company])
        self.assertNotEqual(result.exit_code, 0)
        self.assertEqual(result.output, f'Company {company} not found!\n')
    
if __name__ == '__main__':
    unittest.main() 