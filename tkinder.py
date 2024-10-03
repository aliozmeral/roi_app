import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
import cv2

class ROIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ROI Çizme Uygulaması")

        # Ana pencereyi iki bölüme ayıran frame'ler
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(side="top", fill="x")
        
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(side="bottom", fill="both", expand=True)

        # Koordinatlar ve butonlar alanı (üstte sabit kalan)
        self.coord_label = tk.Label(self.top_frame, text="Koordinatlar: ", anchor="w")
        self.coord_label.pack(side="left", fill="x", expand=False)

        self.reset_button = tk.Button(self.top_frame, text="Sıfırla", command=self.reset_canvas)
        self.reset_button.pack(side="left")

        self.undo_button = tk.Button(self.top_frame, text="Geri", command=self.undo)
        self.undo_button.pack(side="left")
        
        # Kamera veya resim görüntüsünün gösterileceği canvas alanı
        self.canvas = tk.Canvas(self.bottom_frame)
        self.canvas.pack(fill="both", expand=True)

        # Yüklenen resim
        self.image = None
        self.photo = None
        self.image_on_canvas = None
        self.capture = None  # Kamera yakalama nesnesi
        self.is_capturing = False  # Kameradan yakalanıyor mu?

        # Menü oluşturma
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Resim Yükle", command=self.load_image)
        filemenu.add_command(label="Kamera Başlat", command=self.start_camera)
        filemenu.add_command(label="Ekran Görüntüsü Al", command=self.take_screenshot)
        filemenu.add_command(label="Resmi Kaydet", command=self.save_image)
        menubar.add_cascade(label="Dosya", menu=filemenu)
        root.config(menu=menubar)

        # Canvas üzerinde tıklama işlemi için event binding
        self.canvas.bind("<Button-1>", self.draw_roi)
        
        # Önceki nokta (ilk başta None)
        self.previous_point = None

        # Noktaları ve çizgileri kaydetmek için liste
        self.points = []  # Noktaları tutar (x, y)
        self.lines = []   # Çizgileri tutar ((x1, y1), (x2, y2))
        self.shapes = []  # Canvas üzerinde çizilen objeleri takip eder

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            # OpenCV ile resmi yükle
            self.image = cv2.imread(file_path)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            
            # Resmin boyutlarını al
            self.image_height, self.image_width, _ = self.image.shape

            # Resmi PIL formatına dönüştür
            img = Image.fromarray(self.image)
            self.photo = ImageTk.PhotoImage(img)

            # Canvas'ı sıfırla ve canvas'ı resmin boyutlarına göre ayarla
            self.reset_canvas()
            self.canvas.config(width=self.image_width, height=self.image_height)

            # Resmi orijinal boyutlarda canvas'a yerleştir
            self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def start_camera(self):
        """Kamerayı başlat ve canlı akış al"""
        rtsp_link = simpledialog.askstring("RTSP veya Kamera Linki", "Kamera veya RTSP Bağlantısını Girin:")
        if rtsp_link:
            self.capture = cv2.VideoCapture(rtsp_link)
        else:
            self.capture = cv2.VideoCapture(0)  # Web kamerasını başlat
        
        self.is_capturing = True
        self.show_camera_feed()

    def show_camera_feed(self):
        """Kamera görüntüsünü sürekli olarak güncelle"""
        if self.is_capturing and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.image = frame  # Çekilen görüntüyü 'self.image' olarak kaydet
                
                # Kamera çözünürlüğünü al
                self.image_height, self.image_width, _ = frame.shape

                # Canvas boyutlarını kameranın orijinal boyutlarına göre ayarla
                self.canvas.config(width=self.image_width, height=self.image_height)

                # Görüntüyü PIL formatına dönüştür ve canvas üzerinde göster
                img = Image.fromarray(frame)
                self.photo = ImageTk.PhotoImage(img)
                self.reset_canvas()
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

            # Tekrar çağırarak sürekli güncellenmesini sağla
            self.root.after(10, self.show_camera_feed)

    def take_screenshot(self):
        """Kamera görüntüsünden ekran görüntüsü al ve üzerinde çizim yapılmasını sağla"""
        if self.is_capturing:
            self.is_capturing = False
            if self.capture:
                self.capture.release()
            cv2.destroyAllWindows()
            self.update_coord_label()
        
    def draw_roi(self, event):
        # Eğer resim yüklü değilse işlem yapma
        if not self.image_on_canvas:
            return

        # Koordinatları al
        x, y = event.x, event.y

        # Noktayı çiz ve kaydet
        radius = 3
        point_shape = self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline="blue", fill="blue")
        self.points.append((x, y))
        self.shapes.append(point_shape)

        # Noktanın üstüne numara yaz
        point_number = len(self.points)  # Her yeni nokta bir artan numarayla numaralandırılır
        num_text_shape = self.canvas.create_text(x, y - 10, text=str(point_number), fill="red", font=('Helvetica', '12', 'bold'))
        self.shapes.append(num_text_shape)

        # Eğer önceki bir nokta varsa, çizgi çiz ve kaydet
        if self.previous_point is not None:
            x_prev, y_prev = self.previous_point
            line_shape = self.canvas.create_line(x_prev, y_prev, x, y, fill="blue", width=2)
            self.lines.append(((x_prev, y_prev), (x, y)))
            self.shapes.append(line_shape)

        # Koordinatları güncelle ve kaydet
        self.update_coord_label()

        # Yeni noktayı önceki nokta olarak sakla
        self.previous_point = (x, y)

    def update_coord_label(self):
        """Koordinatları güncelleyip Label'da göstermek için fonksiyon"""
        coord_text = "Koordinatlar: "  # Başlangıç metni
        for i, (x, y) in enumerate(self.points):
            coord_text += f"{i + 1} nolu x: {x}, y: {y}   "  # Koordinatları tek satırda boşlukla yaz
        self.coord_label.config(text=coord_text)

    def reset_canvas(self):
        # Canvas'ı temizle ve koordinatları sıfırla
        self.canvas.delete("all")
        self.coord_label.config(text="Koordinatlar: ")
        self.previous_point = None

        # Eğer resim yüklendiyse resmi tekrar göster
        if self.photo:
            self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Noktaları, çizgileri ve şekilleri sıfırla
        self.points = []
        self.lines = []
        self.shapes = []

    def undo(self):
        # Eğer herhangi bir çizim varsa geri alma işlemi yap
        if self.shapes:
            # Son çizgi varsa, hem son çizgiyi hem de son noktayı kaldır
            if len(self.points) > 0:
                last_point_shape = self.shapes.pop()  # Son eklenen noktayı sil
                self.canvas.delete(last_point_shape)  # Canvas üzerinden bu noktayı kaldır
                self.points.pop()  # Son noktayı listeden çıkar

            if len(self.lines) > 0:
                last_line_shape = self.shapes.pop()  # Son eklenen çizgiyi sil
                self.canvas.delete(last_line_shape)  # Canvas üzerinden bu çizgiyi kaldır
                self.lines.pop()  # Son çizgiyi listeden çıkar
            
            # Son nokta olarak bir önceki noktayı sakla
            if len(self.points) > 0:
                self.previous_point = self.points[-1]  # En son noktayı güncelle
            else:
                self.previous_point = None  # Eğer nokta yoksa None yap

            # Geri alma işleminden sonra koordinatları güncelle
            self.update_coord_label()

    def save_image(self):
        if self.image is not None:
            # Yeni bir kopya oluştur
            saved_image = self.image.copy()

            # Font ayarları
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            thickness = 1
            color = (0, 255, 0)  # Yeşil renk
            line_type = cv2.LINE_AA

            # Noktaları ve çizgileri resim üzerinde çiz
            for i, (x, y) in enumerate(self.points):
                # Nokta çiz
                cv2.circle(saved_image, (x, y), 5, (0, 0, 255), -1)  # Kırmızı renkte
                # Noktanın üstüne numara yaz
                cv2.putText(saved_image, str(i + 1), (x, y - 10), font, font_scale, (255, 0, 0), thickness, line_type)
                if i > 0:
                    x_prev, y_prev = self.points[i-1]
                    # Çizgi çiz
                    cv2.line(saved_image, (x_prev, y_prev), (x, y), (255, 0, 0), 2)  # Mavi renkte

            # Koordinatları metin olarak oluştur
            coord_text = [f"{i + 1} nolu x: {x}, y: {y}" for i, (x, y) in enumerate(self.points)]
            
            # Her bir satırı ayrı ayrı çizmek için koordinatları ayarla
            start_x = 10  # Metni yazmaya sol alt köşeden başla
            start_y = saved_image.shape[0] - 20  # Metni aşağıdan yukarı doğru yaz

            for i, text in enumerate(coord_text):
                # Satırları belirli bir aralıkla çiz
                cv2.putText(saved_image, text, (start_x, start_y - i * 20), font, font_scale, color, thickness, line_type)

            # Dosya kaydetme
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if save_path:
                saved_image = cv2.cvtColor(saved_image, cv2.COLOR_RGB2BGR)  # Renkleri BGR'ye çevirme
                cv2.imwrite(save_path, saved_image)

# Ana uygulama
root = tk.Tk()
app = ROIApp(root)
root.mainloop()
