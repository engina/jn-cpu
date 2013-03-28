import unittest
import sys
import ass

class TestOperand(unittest.TestCase):
    def testRegVals(self):
        self.assertEqual(0x00, ass.Operand('A').val)
        self.assertEqual(0x01, ass.Operand('X').val)
        self.assertEqual(0x02, ass.Operand('Y').val)
        self.assertEqual(0x03, ass.Operand('SP').val)
        self.assertEqual(0x04, ass.Operand('PC').val)
        self.assertEqual(0x05, ass.Operand('SR').val)
        self.assertEqual(0x06, ass.Operand('R0').val)
        self.assertEqual(0x07, ass.Operand('R1').val)
        self.assertEqual(0x08, ass.Operand('R2').val)
        self.assertEqual(0x09, ass.Operand('R3').val)
        self.assertEqual(0x0A, ass.Operand('R4').val)
        self.assertEqual(0x0B, ass.Operand('R5').val)
        self.assertEqual(0x0C, ass.Operand('R6').val)
        self.assertEqual(0x0D, ass.Operand('R7').val)
        self.assertEqual(0x0E, ass.Operand('R8').val)
        self.assertEqual(0x0F, ass.Operand('R9').val)

    def testModes(self):
        self.assertEqual(ass.ADDR_IND32, ass.Operand('*0x100').mode)
        self.assertEqual(ass.ADDR_IMM8, ass.Operand('#123').mode)
        self.assertEqual(ass.ADDR_IMM8, ass.Operand('#-123').mode)
        self.assertEqual(ass.ADDR_IMM16, ass.Operand('#-128').mode)
        self.assertEqual(ass.ADDR_IMM16, ass.Operand('#128').mode)
        self.assertEqual(ass.ADDR_IMM16, ass.Operand('#323').mode)
        self.assertEqual(ass.ADDR_IMM32, ass.Operand('#70000').mode)
        self.assertEqual(ass.ADDR_IDX8_X, ass.Operand('X + 10').mode)
        self.assertEqual(ass.ADDR_IDX8_X, ass.Operand('Y + 10').mode)
        self.assertEqual(ass.ADDR_IDX8_X, ass.Operand('SP + 10').mode)
        self.assertEqual(ass.ADDR_IDX8_X, ass.Operand('PC + 10').mode)
        self.assertEqual(ass.ADDR_IDX16_X, ass.Operand('X + 210').mode)
        self.assertEqual(ass.ADDR_IDX16_X, ass.Operand('Y + 210').mode)
        self.assertEqual(ass.ADDR_IDX16_X, ass.Operand('SP + 210').mode)
        self.assertEqual(ass.ADDR_IDX16_X, ass.Operand('PC + 210').mode)
        self.assertEqual(ass.ADDR_DIR32, ass.Operand('10').mode)
        self.assertEqual(ass.ADDR_DIR32, ass.Operand('X').mode)

    def testCornerCases(self):
        # Registers can only be used in indexed mode or reg-to-reg instructions
        self.assertRaises(Exception, lambda: ass.Operand('*X'))
        # Plain invalid
        self.assertRaises(Exception, lambda: ass.Operand('foo'))
        # Indexed addressing mode requires two sub operands
        self.assertRaises(Exception, lambda: ass.Operand('X + Y + A'))
        # Only X, Y, SP, PC can be used as index base.
        self.assertRaises(Exception, lambda: ass.Operand('A + 10'))