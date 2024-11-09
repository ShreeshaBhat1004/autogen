# filename: enhanced_weather_report_with_default_image.py

from fpdf import FPDF
import os

class WeatherReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Calgary Weather Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_weather_section(self, date, temperature, snow, image_path, default_image):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, f'Date: {date}', 0, 1, 'L')
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f'Temperature: {temperature}', 0, 1, 'L')
        self.cell(0, 10, f'Snow: {snow}', 0, 1, 'L')
        self.ln(5)  # Add some space before the image

        # Check if the image file exists, if not use the default image
        img = image_path if os.path.exists(image_path) else default_image
        self.image(img, x=10, y=self.get_y(), w=100)
        self.ln(65)  # Adjust this value to manage space between sections

def create_weather_report():
    pdf = WeatherReportPDF()
    pdf.add_page()

    default_image = 'default_image.jpg'  # Ensure this default image is available

    # Sample data for each day, replace with actual data
    forecast_data = [
        {'date': 'Sat, Nov 9', 'temperature': '44°F / 29°F', 'snow': '0%', 'image': 'image1.jpg'},
        {'date': 'Sun, Nov 10', 'temperature': '42°F / 33°F', 'snow': '0%', 'image': 'image2.jpg'},
        {'date': 'Mon, Nov 11', 'temperature': '54°F / 30°F', 'snow': '2%', 'image': 'image3.jpg'},
        {'date': 'Tue, Nov 12', 'temperature': '47°F / 27°F', 'snow': '1%', 'image': 'image4.jpg'},
        {'date': 'Wed, Nov 13', 'temperature': '41°F / 29°F', 'snow': '1%', 'image': 'image5.jpg'},
        {'date': 'Thu, Nov 14', 'temperature': '42°F / 26°F', 'snow': '2%', 'image': 'image6.jpg'},
        {'date': 'Fri, Nov 15', 'temperature': '32°F / 24°F', 'snow': '2%', 'image': 'image7.jpg'},
    ]

    for day in forecast_data:
        pdf.add_weather_section(day['date'], day['temperature'], day['snow'], day['image'], default_image)

    pdf.output('calgary_weather_report.pdf')

# Generate the PDF weather report
create_weather_report()