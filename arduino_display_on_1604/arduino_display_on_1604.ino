#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);  

void setup() 
{
  lcd.begin(16,4);
  Serial.begin(115200);
  Serial.setTimeout(1);  

  lcd.setCursor(1, 0);
  lcd.print("usamaDEVahmed");
  lcd.setCursor(0, 2);
  lcd.print("CPU: ");
  lcd.setCursor(0, 3);
  lcd.print("GPU: ");
}

void loop() 
{ 
  String line = "";
  String oldCpuLine = "";
  String oldGpuLine = "";
  while (Serial.available() > 0)
  {
    char c = Serial.read();
    if (c == 'S')
    {
      if (!oldCpuLine.equals(line))
      {
        clear(2, 5);
        lcd.setCursor(5, 2);
        lcd.print(line);
        line = ""; 
      }
    }
    else if (c == 'e')
    {
      if (!oldGpuLine.equals(line))
      {
        clear(3, 5);
        lcd.setCursor(5, 3);
        lcd.print(line);
        line = "";
      }
    }
    else 
    {
      line += c; 
    }
  }
  delay(1000);
}

void clear(int row, int st)
{
  while (st <= 15)
  {
    lcd.setCursor(st, row);
    lcd.print(" ");
    st++;
  }
}
