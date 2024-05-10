# Awesome ANPR (Automatic Number Plate Recognition) System 🚗🔍

Welcome to the ANPR system! This powerful project combines cutting-edge OCR (Optical Character Recognition) technology with state-of-the-art object detection using YOLOv5 to provide accurate and efficient vehicle and number plate recognition.

## Features

- **OCR for Number Plates**: Capture an image of a vehicle's number plate, and our system swiftly processes it through advanced OCR algorithms (PaddleOCR) to extract the plate number.
- **Vehicle Information**: Get detailed information about the vehicle associated with the number plate, including make, model, and registration details.
- **Object Detection**: Utilize YOLOv5's robust object detection capabilities to identify vehicles and number plates within images.
- **Efficient Processing**: Our system is designed for speed and efficiency, ensuring rapid recognition and processing of vehicle data.
- **Web Framework Integration**: Built on the Django web framework, our system provides a seamless user experience with a sleek and intuitive interface.

## Installation

To set up the ANPR system locally, follow these simple steps:

1. Clone this repository to your local machine.
2. Install the necessary dependencies using `pip install -r requirements.txt`.
3. Start the Django server by running `python manage.py runserver`.
  - If the project is giving some error regarding the table please run `python manage.py makemigrations` and `python manage.py migrate`.
5. Open your web browser and navigate to `http://localhost:8000` to access the ANPR system.

## Usage

Using the ANPR system is a breeze:

1. Upload an image containing a vehicle's number plate.
2. Click on the "ANPR" button to perform OCR on the number plate and retrieve vehicle information.
3. For enhanced functionality, try the "Detection" option to detect vehicles and number plates within images.

## Contributing

We welcome contributions from the community to enhance the ANPR system further! Whether it's fixing bugs, adding new features, or improving performance, your contributions are valuable. Please refer to our [Contribution Guidelines](CONTRIBUTING.md) for more details on how to get involved.

## License

This project is licensed under the [MIT License](LICENSE), which means you're free to use, modify, and distribute the code for both personal and commercial purposes.

---

ANPR project! 🚀👨‍💻
