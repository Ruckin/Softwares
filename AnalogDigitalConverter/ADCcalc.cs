using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AnalogDigitalConverter
{
    class ADCcalc
    {
        private const double K_adc = 0.00488758553; // CONSTANT VALUE FOR CONVERTION OF 5 VOLTS BY THE 10 BITS RESOLUTION OF THE ADC CONVERTER
        private readonly double volts;

        public ADCcalc(double volts)
        {

            this.volts = (volts >= 0.0 && volts <= 5.0) ? volts : 2.5;
        
        }

        public int ADCvalue()
        {

            return (int) (volts / K_adc);

        }

    } // END OF CALCULATION CLASS
}
