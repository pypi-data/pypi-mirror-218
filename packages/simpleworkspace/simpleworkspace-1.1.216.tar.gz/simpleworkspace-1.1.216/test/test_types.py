import json
import simpleworkspace as sw
from basetestcase import BaseTestCase
from simpleworkspace.types.byte import ByteUnit, ByteEnum
from simpleworkspace.types.time import TimeEnum, TimeUnit

class TimeTests(BaseTestCase):
    def test_Times_HasCorrectSeconds(self):
        self.assertEqual(TimeEnum.NanoSecond.value  * 2, 0.000000002)
        self.assertEqual(TimeEnum.MicroSecond.value * 2, 0.000002)
        self.assertEqual(TimeEnum.MilliSecond.value * 2, 0.002)
        self.assertEqual(TimeEnum.Second.value      * 2, 2)
        self.assertEqual(TimeEnum.Minute.value      * 2, 120)
        self.assertEqual(TimeEnum.Hour.value        * 2, 7200)
        self.assertEqual(TimeEnum.Day.value         * 2, 172800)
        
    def test_TimeUnit_KnownEqualityChecks(self):
        self.assertEqual(TimeUnit(1000 * 1000 * 1000 * 2, TimeEnum.NanoSecond),
                         TimeUnit(2, TimeEnum.Second))
        self.assertEqual(TimeUnit(1000 * 1000 * 2, TimeEnum.MicroSecond),
                         TimeUnit(2, TimeEnum.Second))
        self.assertEqual(TimeUnit(1000 * 2, TimeEnum.MilliSecond),
                         TimeUnit(2, TimeEnum.Second))
        self.assertEqual(TimeUnit(2, TimeEnum.Minute),
                         TimeUnit(120, TimeEnum.Second))

        convertedUnit = TimeUnit(86400, TimeEnum.Second)
        convertedUnit_toNanoSeconds = convertedUnit.To(TimeEnum.NanoSecond)
        convertedUnit_toMicroSeconds = convertedUnit.To(TimeEnum.MicroSecond)
        convertedUnit_toMilliSeconds = convertedUnit.To(TimeEnum.MilliSecond)
        convertedUnit_toMinute = convertedUnit.To(TimeEnum.Minute)
        convertedUnit_toHour = convertedUnit_toMinute.To(TimeEnum.Hour)
        convertedUnit_toDay = convertedUnit_toHour.To(TimeEnum.Day)
        self.assertEqual(convertedUnit_toNanoSeconds, TimeUnit(1000 * 1000 * 1000 * 86400, TimeEnum.NanoSecond))
        self.assertEqual(convertedUnit_toMicroSeconds, TimeUnit(1000 * 1000 * 86400, TimeEnum.MicroSecond))
        self.assertEqual(convertedUnit_toMilliSeconds, TimeUnit(1000 * 86400, TimeEnum.MilliSecond))
        self.assertEqual(convertedUnit, TimeUnit(86400, TimeEnum.Second))
        self.assertEqual(convertedUnit_toMinute, TimeUnit(1440, TimeEnum.Minute))
        self.assertEqual(convertedUnit_toHour, TimeUnit(24, TimeEnum.Hour))
        self.assertEqual(convertedUnit_toDay, TimeUnit(1, TimeEnum.Day))

        self.assertEqual(TimeUnit(2, TimeEnum.Hour).To(TimeEnum.Minute),
                         TimeUnit(120, TimeEnum.Minute))

    def test_TimeUnit_NegativeEqualityChecks(self):
        self.assertNotEqual(TimeUnit(2, TimeEnum.Minute),
                            TimeUnit(2, TimeEnum.Second))
        
        self.assertNotEqual(TimeUnit(2, TimeEnum.Minute),
                            TimeUnit(3, TimeEnum.Minute))
        
    def test_TimeUnit_StrictEqualityCheck(self):
        t = TimeUnit(86400, TimeEnum.Second).To(TimeEnum.Hour)
        self.assertEqual(t.amount, 24)
        self.assertEqual(t.unit, TimeEnum.Hour)

        t = TimeUnit(24, TimeEnum.Hour).To(TimeEnum.Second)
        self.assertEqual(t.amount, 86400)
        self.assertEqual(t.unit, TimeEnum.Second)


        t = TimeUnit(86400, TimeEnum.Second)
        assert t.To(TimeEnum.NanoSecond ).amount == 1000 * 1000 * 1000 * 86400
        assert t.To(TimeEnum.MicroSecond).amount == 1000 * 1000 * 86400
        assert t.To(TimeEnum.MilliSecond).amount == 1000 * 86400
        assert t.To(TimeEnum.Second     ).amount == 86400
        assert t.To(TimeEnum.Minute     ).amount == 1440
        assert t.To(TimeEnum.Hour       ).amount == 24
        assert t.To(TimeEnum.Day        ).amount == 1

        t = TimeUnit(1440, TimeEnum.Minute)
        assert t.To(TimeEnum.NanoSecond ).amount == 1000 * 1000 * 1000 * 86400
        assert t.To(TimeEnum.MicroSecond).amount == 1000 * 1000 * 86400
        assert t.To(TimeEnum.MilliSecond).amount == 1000 * 86400
        assert t.To(TimeEnum.Second     ).amount == 86400
        assert t.To(TimeEnum.Minute     ).amount == 1440
        assert t.To(TimeEnum.Hour       ).amount == 24
        assert t.To(TimeEnum.Day        ).amount == 1

        t = TimeUnit(24, TimeEnum.Hour)
        assert t.To(TimeEnum.NanoSecond ).amount == 1000 * 1000 * 1000 * 86400
        assert t.To(TimeEnum.MicroSecond).amount == 1000 * 1000 * 86400
        assert t.To(TimeEnum.MilliSecond).amount == 1000 * 86400
        assert t.To(TimeEnum.Second     ).amount == 86400
        assert t.To(TimeEnum.Minute     ).amount == 1440
        assert t.To(TimeEnum.Hour       ).amount == 24
        assert t.To(TimeEnum.Day        ).amount == 1

        t = TimeUnit(1, TimeEnum.Day)
        assert t.To(TimeEnum.NanoSecond ).amount == 1000 * 1000 * 1000 * 86400
        assert t.To(TimeEnum.MicroSecond).amount == 1000 * 1000 * 86400
        assert t.To(TimeEnum.MilliSecond).amount == 1000 * 86400
        assert t.To(TimeEnum.Second     ).amount == 86400
        assert t.To(TimeEnum.Minute     ).amount == 1440
        assert t.To(TimeEnum.Hour       ).amount == 24
        assert t.To(TimeEnum.Day        ).amount == 1

    def test_TimeUnit_ArchimetricOperators(self):
        # Test Inplace Addition with float
        time1 = TimeUnit(1, TimeEnum.Second)
        float_val = 1
        time1 += float_val
        self.assertEqual(time1.amount, 2)
        self.assertEqual(time1.unit, TimeEnum.Second)
        # Test Inplace Addition with another unit
        time1 = TimeUnit(5, TimeEnum.Second)
        time2 = TimeUnit(1, TimeEnum.Minute)
        time3 = TimeUnit(1 * 1000, TimeEnum.MilliSecond)
        time4 = TimeUnit(1 * 1000 * 1000, TimeEnum.MicroSecond)
        time5 = TimeUnit(1 * 1000 * 1000 * 1000, TimeEnum.NanoSecond)
        time1 += time2
        time1 += time3
        time1 += time4
        time1 += time5
        self.assertEqual(time1.amount, 68 )
        self.assertEqual(time1.unit, TimeEnum.Second)


        # Test Inplace Multiplication with float
        time1 = TimeUnit(2, TimeEnum.Minute)
        float_val = 2
        time1 *= float_val
        self.assertEqual(time1.amount, 4)
        # Test Inplace Multiplication with another unit
        time1 = TimeUnit(2, TimeEnum.Minute)
        time2 = TimeUnit(2, TimeEnum.Minute)
        time1 *= time2
        self.assertEqual(time1.amount, 4 )


        # Test Inplace Division with float
        time1 = TimeUnit(6, TimeEnum.Hour)
        float_val = 3
        time1 /= float_val
        self.assertEqual(time1.amount, 2 )
        # Test Inplace Division with another unit
        time1 = TimeUnit(2, TimeEnum.Hour)
        time2 = TimeUnit(60, TimeEnum.Minute)
        time1 /= time2
        self.assertEqual(time1.amount, 2)


        # Test Inplace Subtraction with float
        time1 = TimeUnit(3, TimeEnum.Second)
        float_val = 1.0
        time1 -= float_val
        self.assertEqual(time1.amount, 2.0 )
        # Test Inplace Subtraction with another unit
        time1 = TimeUnit(65, TimeEnum.Second)
        time2 = TimeUnit(1, TimeEnum.Minute)
        time1 -= time2
        self.assertEqual(time1.amount, 5)        

    def test_timeUnit_getparts(self):
        # Test case 1
        parts = TimeUnit(2.5, TimeEnum.Minute).GetParts()
        self.assertEqual(parts, {
            TimeEnum.NanoSecond: 0.0,
            TimeEnum.MicroSecond: 0.0,
            TimeEnum.MilliSecond: 0.0,
            TimeEnum.Second: 30,
            TimeEnum.Minute: 2.0,
            TimeEnum.Hour: 0.0,
            TimeEnum.Day: 0.0
        })

        # Test case 2
        parts = TimeUnit(90, TimeEnum.Second).GetParts()
        self.assertEqual(parts, {
            TimeEnum.NanoSecond: 0.0,
            TimeEnum.MicroSecond: 0.0,
            TimeEnum.MilliSecond: 0.0,
            TimeEnum.Second: 30.0,
            TimeEnum.Minute: 1.0,
            TimeEnum.Hour: 0.0,
            TimeEnum.Day: 0.0
        })

        # Test case 3
        parts = TimeUnit(3601, TimeEnum.Second).GetParts()
        self.assertEqual(parts, {
            TimeEnum.NanoSecond: 0.0,
            TimeEnum.MicroSecond: 0.0,
            TimeEnum.MilliSecond: 0.0,
            TimeEnum.Second: 1.0,
            TimeEnum.Minute: 0.0,
            TimeEnum.Hour: 1.0,
            TimeEnum.Day: 0.0
        })


        # Test case 4
        parts = TimeUnit(62.1002003, TimeEnum.Second).GetParts()
        parts[TimeEnum.NanoSecond] = round(parts[TimeEnum.NanoSecond]) # get rid of insanely low decimals after division operations
        self.assertEqual(parts, {
            TimeEnum.NanoSecond: 300.0,
            TimeEnum.MicroSecond: 200.0,
            TimeEnum.MilliSecond: 100.0,
            TimeEnum.Second: 2.0,
            TimeEnum.Minute: 1.0,
            TimeEnum.Hour: 0.0,
            TimeEnum.Day: 0.0
        })

        # Test case 5: maxPart
        parts = TimeUnit(1, TimeEnum.Day).GetParts(maxPart=TimeEnum.Hour)
        parts[TimeEnum.NanoSecond] = round(parts[TimeEnum.NanoSecond]) # get rid of insanely low decimals after division operations
        self.assertEqual(parts, {
            TimeEnum.NanoSecond : 0.0,
            TimeEnum.MicroSecond: 0.0,
            TimeEnum.MilliSecond: 0.0,
            TimeEnum.Second     : 0.0,
            TimeEnum.Minute     : 0.0,
            TimeEnum.Hour       : 24.0,
        })

        # Test case 5: minPart
        parts = TimeUnit(2.5, TimeEnum.Minute).GetParts(minPart=TimeEnum.Minute)
        parts[TimeEnum.Minute] = round(parts[TimeEnum.Minute],6) # get rid of insanely low decimals after division operations
        self.assertEqual(parts, {
            TimeEnum.Minute     : 2.5,
            TimeEnum.Hour       : 0.0,
            TimeEnum.Day        : 0.0
        })

        # Test case 5: minPart and maxPart
        parts = TimeUnit(3601.1, TimeEnum.Second).GetParts(minPart=TimeEnum.Second, maxPart=TimeEnum.Minute)
        parts[TimeEnum.Second] = round(parts[TimeEnum.Second],6) # get rid of insanely low decimals after division operations
        self.assertEqual(parts, {
            TimeEnum.Second     : 1.1,
            TimeEnum.Minute     : 60.0,
        })



   
class ByteTests(BaseTestCase):
    def test_ByteUnit_Conversions_KnownEqualityChecks(self):
        # Test conversions from Byte to other units
        self.assertEqual(ByteUnit(1, ByteEnum.Byte).To(ByteEnum.Bit), 
                         ByteUnit(8, ByteEnum.Bit))

        self.assertEqual(ByteUnit(1, ByteEnum.Byte).To(ByteEnum.KiloByte), 
                         ByteUnit(0.001, ByteEnum.KiloByte))
        
        self.assertEqual(ByteUnit(1, ByteEnum.Byte).To(ByteEnum.MegaByte),
                         ByteUnit(0.000001, ByteEnum.MegaByte))
        
        self.assertEqual(ByteUnit(1, ByteEnum.Byte).To(ByteEnum.GigaByte), 
                         ByteUnit(0.000000001, ByteEnum.GigaByte))
        
        self.assertEqual(ByteUnit(1, ByteEnum.Byte).To(ByteEnum.TeraByte), 
                         ByteUnit(0.000000000001, ByteEnum.TeraByte))

        # Test conversions from KiloByte to other units
        self.assertEqual(ByteUnit(1000, ByteEnum.KiloByte).To(ByteEnum.Byte), 
                         ByteUnit(1000000, ByteEnum.Byte))
        
        self.assertEqual(ByteUnit(1000, ByteEnum.KiloByte).To(ByteEnum.MegaByte), 
                         ByteUnit(1, ByteEnum.MegaByte))
        
        self.assertEqual(ByteUnit(1000, ByteEnum.KiloByte).To(ByteEnum.GigaByte), 
                         ByteUnit(0.001, ByteEnum.GigaByte))
        
        self.assertEqual(ByteUnit(1000, ByteEnum.KiloByte).To(ByteEnum.TeraByte), 
                         ByteUnit(0.000001, ByteEnum.TeraByte))

        # Test conversions from MegaByte to other units
        self.assertEqual(ByteUnit(1000, ByteEnum.MegaByte).To(ByteEnum.Byte), 
                         ByteUnit(1000000000, ByteEnum.Byte))
        
        self.assertEqual(ByteUnit(1000, ByteEnum.MegaByte).To(ByteEnum.KiloByte), 
                         ByteUnit(1000000, ByteEnum.KiloByte))
        
        self.assertEqual(ByteUnit(1000, ByteEnum.MegaByte).To(ByteEnum.GigaByte), 
                         ByteUnit(1, ByteEnum.GigaByte))
        
        self.assertEqual(ByteUnit(1000, ByteEnum.MegaByte).To(ByteEnum.TeraByte), 
                         ByteUnit(0.001, ByteEnum.TeraByte))

        # Test conversions from GigaByte to other units
        self.assertEqual(ByteUnit(1000, ByteEnum.GigaByte).To(ByteEnum.Byte), 
                         ByteUnit(1000000000000, ByteEnum.Byte))
        
        self.assertEqual(ByteUnit(1000, ByteEnum.GigaByte).To(ByteEnum.KiloByte), 
                         ByteUnit(1000000000, ByteEnum.KiloByte))
        
        self.assertEqual(ByteUnit(1000, ByteEnum.GigaByte).To(ByteEnum.MegaByte), 
                         ByteUnit(1000000, ByteEnum.MegaByte))
        
        self.assertEqual(ByteUnit(1000, ByteEnum.GigaByte).To(ByteEnum.TeraByte), 
                         ByteUnit(1, ByteEnum.TeraByte))

        # Test conversions from TerraByte to other units
        self.assertEqual(ByteUnit(1000, ByteEnum.TeraByte).To(ByteEnum.Byte), 
                         ByteUnit(1000000000000000, ByteEnum.Byte))
        
        self.assertEqual(ByteUnit(1000, ByteEnum.TeraByte).To(ByteEnum.KiloByte), 
                         ByteUnit(1000000000000, ByteEnum.KiloByte))
        
        self.assertEqual(ByteUnit(1000, ByteEnum.TeraByte).To(ByteEnum.MegaByte), 
                         ByteUnit(1000000000, ByteEnum.MegaByte))
        
        self.assertEqual(ByteUnit(1000, ByteEnum.TeraByte).To(ByteEnum.GigaByte), 
                         ByteUnit(1000000, ByteEnum.GigaByte))


        # Test conversions between all possible units
        self.assertEqual(ByteUnit(1024, ByteEnum.Bit).To(ByteEnum.Byte),
                         ByteUnit(128, ByteEnum.Byte))
        
        self.assertEqual(ByteUnit(1024, ByteEnum.Byte).To(ByteEnum.KiloByte),
                         ByteUnit(1.024, ByteEnum.KiloByte))
        
        self.assertEqual(ByteUnit(1.024, ByteEnum.KiloByte).To(ByteEnum.Byte),
                         ByteUnit(1024, ByteEnum.Byte))
        
        self.assertEqual(ByteUnit(1, ByteEnum.MegaByte).To(ByteEnum.GigaByte),
                         ByteUnit(0.001, ByteEnum.GigaByte))
        
        self.assertEqual(ByteUnit(100, ByteEnum.GigaByte).To(ByteEnum.TeraByte),
                         ByteUnit(0.1, ByteEnum.TeraByte))
        
        self.assertEqual(ByteUnit(2000, ByteEnum.KiloByte).To(ByteEnum.MegaByte),
                        ByteUnit(2, ByteEnum.MegaByte))
        
        self.assertEqual(ByteUnit(2, ByteEnum.MegaByte).To(ByteEnum.KiloByte),
                         ByteUnit(2000, ByteEnum.KiloByte))
        
    def test_ByteUnit_NegativeEqualityChecks(self):
        # Test conversions between all possible units
        self.assertNotEqual(ByteUnit(1024, ByteEnum.Byte).To(ByteEnum.KiloByte),
                         ByteUnit(1024, ByteEnum.KiloByte))
        
        self.assertNotEqual(ByteUnit(1.024, ByteEnum.KiloByte).To(ByteEnum.Byte),
                         ByteUnit(1.024, ByteEnum.Byte))
        
        self.assertNotEqual(ByteUnit(1, ByteEnum.MegaByte).To(ByteEnum.GigaByte),
                         ByteUnit(1, ByteEnum.GigaByte))
        
        self.assertNotEqual(ByteUnit(100, ByteEnum.GigaByte).To(ByteEnum.TeraByte),
                         ByteUnit(100, ByteEnum.TeraByte))
        
        self.assertNotEqual(ByteUnit(2000, ByteEnum.KiloByte).To(ByteEnum.MegaByte),
                        ByteUnit(2000, ByteEnum.MegaByte))
        
        self.assertNotEqual(ByteUnit(2, ByteEnum.MegaByte).To(ByteEnum.KiloByte),
                         ByteUnit(2, ByteEnum.KiloByte))

    def test_ByteUnit_EqualityChecksWithDiffentUnits(self):
        # Test conversions between all possible units
        self.assertEqual(ByteUnit(1024, ByteEnum.Byte),
                         ByteUnit(1.024, ByteEnum.KiloByte))
        
        self.assertEqual(ByteUnit(1.024, ByteEnum.KiloByte),
                         ByteUnit(1024, ByteEnum.Byte))
        
        self.assertEqual(ByteUnit(1, ByteEnum.MegaByte),
                         ByteUnit(0.001, ByteEnum.GigaByte))
        
        self.assertEqual(ByteUnit(100, ByteEnum.GigaByte),
                         ByteUnit(0.1, ByteEnum.TeraByte))
        
        self.assertEqual(ByteUnit(2000, ByteEnum.KiloByte),
                        ByteUnit(2, ByteEnum.MegaByte))
        
        self.assertEqual(ByteUnit(2, ByteEnum.MegaByte),
                         ByteUnit(2000, ByteEnum.KiloByte))
        
    def test_ByteUnit_StrictEqualityCheck(self):
        byteUnit = ByteUnit(5, ByteEnum.MegaByte)
        self.assertEqual(byteUnit.To(ByteEnum.Bit     ).amount, 40000000)
        self.assertEqual(byteUnit.To(ByteEnum.Byte    ).amount, 5000000)
        self.assertEqual(byteUnit.To(ByteEnum.KiloByte).amount, 5000)
        self.assertEqual(byteUnit.To(ByteEnum.MegaByte).amount, 5)
        self.assertEqual(byteUnit.To(ByteEnum.GigaByte).amount, 0.005)
        self.assertEqual(byteUnit.To(ByteEnum.TeraByte).amount, 0.000005)

        # Test conversions between all possible units
        convertedUnit = ByteUnit(8192, ByteEnum.Bit).To(ByteEnum.KiloByte)
        self.assertEqual(convertedUnit.amount, 1.024)
        self.assertEqual(convertedUnit.unit, ByteEnum.KiloByte)

        convertedUnit = ByteUnit(1024, ByteEnum.Byte).To(ByteEnum.KiloByte)
        self.assertEqual(convertedUnit.amount, 1.024)
        self.assertEqual(convertedUnit.unit, ByteEnum.KiloByte)

        convertedUnit = ByteUnit(1.024, ByteEnum.KiloByte).To(ByteEnum.Byte)
        self.assertEqual(convertedUnit.amount, 1024)
        self.assertEqual(convertedUnit.unit, ByteEnum.Byte)

        convertedUnit = ByteUnit(1, ByteEnum.MegaByte).To(ByteEnum.GigaByte)
        self.assertEqual(convertedUnit.amount, 0.001)
        self.assertEqual(convertedUnit.unit, ByteEnum.GigaByte)

        convertedUnit = ByteUnit(100, ByteEnum.GigaByte).To(ByteEnum.TeraByte)
        self.assertEqual(convertedUnit.amount, 0.1)
        self.assertEqual(convertedUnit.unit, ByteEnum.TeraByte)

        convertedUnit = ByteUnit(2000, ByteEnum.KiloByte).To(ByteEnum.MegaByte)
        self.assertEqual(convertedUnit.amount, 2)
        self.assertEqual(convertedUnit.unit, ByteEnum.MegaByte)

        convertedUnit = ByteUnit(2, ByteEnum.MegaByte).To(ByteEnum.KiloByte)
        self.assertEqual(convertedUnit.amount, 2000)
        self.assertEqual(convertedUnit.unit, ByteEnum.KiloByte)
    
    def test_ByteUnit_ArchimetricOperators(self):
        # Test Inplace Addition with float
        byte1 = ByteUnit(1, ByteEnum.KiloByte)
        float_val = 1
        byte1 += float_val
        self.assertEqual(byte1.amount, 2)
        self.assertEqual(byte1.unit, ByteEnum.KiloByte)
        # Test Inplace Addition with another unit
        byte1 = ByteUnit(1, ByteEnum.KiloByte)
        byte2 = ByteUnit(500, ByteEnum.Byte)
        byte1 += byte2
        self.assertEqual(byte1.amount, 1.5 )
        self.assertEqual(byte1.unit, ByteEnum.KiloByte)


        # Test Inplace Multiplication with float
        byte1 = ByteUnit(2, ByteEnum.KiloByte)
        float_val = 2
        byte1 *= float_val
        self.assertEqual(byte1.amount, 4)
        # Test Inplace Multiplication with another unit
        byte1 = ByteUnit(2, ByteEnum.KiloByte)
        byte2 = ByteUnit(2, ByteEnum.KiloByte)
        byte1 *= byte2
        self.assertEqual(byte1.amount, 4 )


        # Test Inplace Division with float
        byte1 = ByteUnit(6, ByteEnum.MegaByte)
        float_val = 3
        byte1 /= float_val
        self.assertEqual(byte1.amount, 2 )
        # Test Inplace Division with another unit
        byte1 = ByteUnit(6, ByteEnum.MegaByte)
        byte2 = ByteUnit(3000, ByteEnum.KiloByte)
        byte1 /= byte2
        self.assertEqual(byte1.amount, 2)


        # Test Inplace Subtraction with float
        byte1 = ByteUnit(3, ByteEnum.KiloByte)
        float_val = 1.0
        byte1 -= float_val
        self.assertEqual(byte1.amount, 2.0 )
        # Test Inplace Subtraction with another unit
        byte1 = ByteUnit(1, ByteEnum.GigaByte)
        byte2 = ByteUnit(500, ByteEnum.MegaByte)
        byte1 -= byte2
        self.assertEqual(byte1.amount, 0.5)

    def test_byteUnit_getparts(self):
        # Test case 1
        parts =  ByteUnit(1.5, ByteEnum.MegaByte).GetParts()
        self.assertEqual(parts, {
            ByteEnum.Bit: 0.0,
            ByteEnum.Byte: 0.0,
            ByteEnum.KiloByte: 500.0,
            ByteEnum.MegaByte: 1.0,
            ByteEnum.GigaByte: 0.0,
            ByteEnum.TeraByte: 0.0,
            ByteEnum.PetaByte: 0.0,
            ByteEnum.ExaByte: 0.0,
        })

        #test case 2, maxpart
        parts =  ByteUnit(1.5, ByteEnum.MegaByte).GetParts(maxPart=ByteEnum.KiloByte)
        self.assertEqual(parts, {
            ByteEnum.Bit: 0.0,
            ByteEnum.Byte: 0.0,
            ByteEnum.KiloByte: 1500.0,
        })

        #test case 3, minpart
        parts =  ByteUnit(1500, ByteEnum.KiloByte).GetParts(minPart=ByteEnum.MegaByte)
        self.assertEqual(parts, {
            ByteEnum.MegaByte: 1.5,
            ByteEnum.GigaByte: 0.0,
            ByteEnum.TeraByte: 0.0,
            ByteEnum.PetaByte: 0.0,
            ByteEnum.ExaByte: 0.0,
        })


        #test case 4, minpart & maxpart
        parts =  ByteUnit(1002.1, ByteEnum.MegaByte).GetParts(minPart=ByteEnum.MegaByte, maxPart=ByteEnum.GigaByte)
        self.assertEqual(parts, {
            ByteEnum.MegaByte: 2.1,
            ByteEnum.GigaByte: 1.0,
        })

