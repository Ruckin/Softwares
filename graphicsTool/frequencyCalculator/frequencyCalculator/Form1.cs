using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace frequencyCalculator
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {

            float resistor, capacitor, frequency;

            resistor = float.Parse(resValue.Text);
            capacitor = float.Parse(capValue.Text);

            frequency = 1 / (2 * 3.14159f * resistor * capacitor);

            freqValue.Text = frequency.ToString();

        }
    }
}
