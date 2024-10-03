
# ROI Çizme Uygulaması

Bu uygulama, kullanıcıların görüntüler üzerinde `ROI (Region of Interest)` alanları çizmesine olanak tanır. Uygulama, yerel resim dosyalarını açarak veya bir kamera / RTSP bağlantısından canlı görüntü alarak çalışır. Ayrıca kullanıcılar ekran görüntüsü alabilir ve bu görüntü üzerinde çizimler yapabilirler.

## Özellikler
- Yerel bir resim dosyasını yükleyin ve üzerine çizim yapın.
- Web kamerası veya RTSP bağlantısı üzerinden gelen canlı görüntüyü görüntüleyin.
- Çizim yaparken koordinatları ekranda gösterin.
- Yaptığınız çizimleri `.png` formatında kaydedin.
- Geri alma ve sıfırlama seçenekleri.

## Kurulum
Uygulamayı çalıştırmak için aşağıdaki adımları izleyin:

1. Gerekli bağımlılıkları yükleyin:

   ```bash
   pip install -r requirements.txt
   ```

   **Gereksinimler**:
   - OpenCV (`cv2`)
   - Pillow (Python Imaging Library - PIL)
   - Tkinter (genellikle Python ile birlikte gelir)

2. Uygulamayı çalıştırın:

   ```bash
   python tikender.py
   ```

## Kullanım
1. Uygulamayı başlattıktan sonra, `Dosya` menüsünden:
   - **Resim Yükle**: Bilgisayarınızdan bir resim dosyası seçip açın.
   - **Kamera Başlat**: Web kamerasını başlatın veya bir RTSP bağlantısı girin.
   - **Ekran Görüntüsü Al**: Kameradan alınan canlı görüntüyü durdurun ve çizim yapmaya başlayın.
   - **Resmi Kaydet**: Çizim yaptığınız resmi `.png` formatında kaydedin.
2. Çizim sırasında, koordinatlar üst menüde görüntülenir. `Geri` butonuyla son çizimi geri alabilir, `Sıfırla` butonuyla tüm çizimleri temizleyebilirsiniz.

## EXE Olarak Çalıştırma
Bu Python uygulamasını `.exe` dosyasına dönüştürmek için aşağıdaki adımları takip edin:

1. PyInstaller'ı yükleyin:

   ```bash
   pip install pyinstaller
   ```

2. Uygulamanızı `.exe` dosyasına dönüştürün:

   ```bash
   pyinstaller --onefile --windowed your_script.py
   ```

3. `.exe` dosyanız `dist` klasöründe bulunacaktır.

## Katkıda Bulunma
Katkıda bulunmak isterseniz, lütfen bir pull request oluşturun veya bir konu açın.

## Lisans
Bu proje MIT Lisansı ile lisanslanmıştır.


# ROI Drawing Application

This application allows users to draw `Region of Interest (ROI)` areas on images. The application works by loading local image files or by capturing live video from a camera or an RTSP stream. Additionally, users can take screenshots and draw on those images.

## Features
- Load a local image file and draw on it.
- Display live video from a webcam or an RTSP stream.
- Show coordinates while drawing on the image.
- Save the drawings in `.png` format.
- Undo and reset drawing options.

## Installation
To run the application, follow these steps:

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   **Requirements**:
   - OpenCV (`cv2`)
   - Pillow (Python Imaging Library - PIL)
   - Tkinter (usually comes with Python)

2. Run the application:

   ```bash
   python your_script.py
   ```

## Usage
1. After starting the application, from the `File` menu:
   - **Load Image**: Choose and open an image file from your computer.
   - **Start Camera**: Start the webcam or enter an RTSP stream URL.
   - **Take Screenshot**: Stop the live video feed and begin drawing on the captured image.
   - **Save Image**: Save the image with your drawings in `.png` format.
2. While drawing, the coordinates are displayed in the top menu. You can undo the last drawing using the `Undo` button, or clear all drawings with the `Reset` button.

## Running as an EXE
To convert this Python application into a `.exe` file, follow these steps:

1. Install PyInstaller:

   ```bash
   pip install pyinstaller
   ```

2. Convert the application to a `.exe` file:

   ```bash
   pyinstaller --onefile --windowed your_script.py
   ```

3. The `.exe` file will be located in the `dist` folder.

## Contributing
If you'd like to contribute, feel free to open a pull request or issue.

## License
This project is licensed under the MIT License.
