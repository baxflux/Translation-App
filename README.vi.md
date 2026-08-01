<a id="readme-top"></a>

<h1 align="center">Translation App</h1>

<h4 align="center">
  <em>Ứng dụng dịch thuật từ tiếng Anh sang tiếng Việt</em>
</h4>

<div align="center">
  <a href="README.md"><strong>Tiếng Anh</strong></a> 
  •
  <strong>Tiếng Việt</strong>
</div>

<br>

## Mục lục

- [Giới thiệu tổng quát](#giới-thiệu-tổng-quát)
- [Tập dữ liệu](#tập-dữ-liệu)
- [Kết quả đạt được](#kết-quả-đạt-được)
- [Công nghệ tiêu biểu](#công-nghệ-tiêu-biểu)
- [Cấu trúc mã nguồn](#cấu-trúc-mã-nguồn)
- [Khởi động dự án](#khởi-động-dự-án)
- [Giấy phép](#giấy-phép)

## Giới thiệu tổng quát

Đây là dự án xây dựng một **Web App dịch thuật văn bản một chiều từ tiếng Anh sang tiếng Việt**, dựa trên mô hình ngôn ngữ lớn **Qwen2.5-0.5B**, được Finetune trên tập dữ liệu song ngữ Anh - Việt bằng các kỹ thuật để tối ưu tài nguyên.

Dưới đây là phần tóm tắt toàn bộ quy trình xây dựng dự án:

<div align="center">
  <a href="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/translation_app.png" target="_blank">
    <img src="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/translation_app.png"
         alt="Kiến trúc tổng thể của dự án Translation App" width="700">
  </a>
</div>

<p align="center">
  <strong>Hình 1:</strong> Kiến trúc tổng thể của dự án Translation App
</p>

Bước đầu tiên của dự án là **phân tích khám phá dữ liệu** (Exploratory Data Analysis – EDA) đối với tập dữ liệu song ngữ, quá trình này diễn ra trên nền tảng **Kaggle** (trang Web cung cấp một lượng lớn GPU miễn phí) từ đó đưa ra được những kết luận quan trọng về phân bố chiều dài của cặp văn bản song ngữ.

Tiếp theo là bước xây dựng mô hình, cũng diễn ra trên Kaggle. Mặc dù tập dữ liệu được chia sẵn từ Hugging Face, ta sẽ chỉ lấy một phần nhỏ vì vấn đề tài nguyên, với phân bố Train/Validation/Test tương ứng với **25000/2000/2000 mẫu** dữ liệu. Sau đó sẽ tiến hành lọc dữ liệu theo độ dài Token để mô hình có thể học hiệu quả:

1. Câu tiếng Anh có độ dài trong khoảng **(5, 40)** Token
2. Câu tiếng Việt có độ dài trong khoảng **(5, 50)** Token

Sau đó tiến hành điều chỉnh **Prompt** để phù hợp với cấu trúc của mô hình Qwen, cũng như xây dựng **Tokenization** cho tập Train và Validation để đảm bảo tính nhất quán của dữ liệu khi huấn luyện. Bước tiếp theo là tải mô hình Base **Qwen2.5-0.5B**, kết hợp với việc cấu hình kỹ thuật **LoRA (Low-Rank Adaptation)** để Finetune mô hình được tốt hơn. Nói thêm một chút, kỹ thuật này cho phép:

1. Giảm số lượng tham số cần huấn luyện.
2. Tiết kiệm bộ nhớ GPU.
3. Phù hợp với môi trường huấn luyện có tài nguyên hạn chế.

Sau bước này thì vào giai đoạn cấu hình tham số huấn luyện bằng thư viện **TrainingArguments**, và huấn luyện bằng **SFTTrainer**. Trong suốt quá trình huấn luyện, các đoạn **Log** được ghi lại để đánh giá mô hình bằng nhiều biểu đồ khác nhau (Accuracy/Loss). Ngoài ra, ta cũng sử dụng các chỉ số như **BLEU** và **ROUGE** khi đánh giá trên tập dữ liệu Test để xem khả năng tổng quát hoá và chất lượng dịch thuật của mô hình.

Để thử nghiệm với dữ liệu mới (Inference), ta đưa vào một câu tiếng Anh cơ bản. Tiến hành tải lại mô hình Base và mô hình mới vừa được Finetune, sau đó áp dụng Prompt và Tokenizer đã được xây dựng từ trước để xem được bản dịch tiếng Việt tương ứng. Kết thúc của quá trình huấn luyện chính là đóng gói mô hình thành Zip để tiện cho việc tải xuống.

Bước thứ hai, tải mô hình đã đóng gói vào phần Web App được xây dựng từ **Flask** Backend, kết hợp với giao diện **HTML** đơn giản. Khi tương tác trên trình duyệt, ta nhập vào văn bản là tiếng Anh thì kết quả nhận được kết quả chính là văn bản dịch thuật bằng tiếng Việt.

<div align="right">
  <a href="#readme-top">↑ Quay lại đầu trang</a>
</div>

## Tập dữ liệu

[![Dataset](https://img.shields.io/badge/Dataset-0A66C2?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/datasets/ncduy/mt-en-vi)

Tập dữ liệu của dự án này có tên là **mt-en-vi**, một tập dữ liệu song ngữ Anh – Việt (English – Vietnamese), liên quan đến những văn bản song ngữ được tổng hợp từ nhiều nguồn tiếng Anh - Việt khác nhau. Tập dữ liệu nằm trên trang Web Hugging Face, nơi lưu trữ các tập dữ liệu cũng như mô hình nổi tiếng và uy tín.

**Thông tin mô tả của Dataset:** Chứa những cặp câu song song giữa hai ngôn ngữ Anh - Việt, với ba thuộc tính chính:

1. **en:** Câu văn bản bằng tiếng Anh.
2. **vi:** Câu văn bản bằng tiếng Việt.
3. **source:** Nguồn gốc của cặp câu song ngữ (OpenSubtitles v2018, TED2020 v1, QED v2.0a, WikiMatrix v1, wikimedia v20210402, vietnamsongngu.com, baosongngu.net, Tatoeba v2021-07-22)

Tập dữ liệu này đã được chia sẵn trên Hugging Face thành ba tập **Train/Validation/Test**, do đó trong quá trình sử dụng có thể không cần tự chia lại dữ liệu.

<div align="right">
  <a href="#readme-top">↑ Quay lại đầu trang</a>
</div>

## Kết quả đạt được

Đầu tiên là một số biểu đồ trực quan về quá trình huấn luyện mô hình:

<table>
  <tr>
    <td width="47%" align="center" valign="bottom">
      <a href="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/token_accuracy.png">
        <img src="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/token_accuracy.png" alt="Token Accuracy của mô hình">
      </a>
      <br>
      <strong>Hình 2:</strong> Token Accuracy của mô hình
    </td>
    <td width="53%" align="center" valign="bottom">
      <a href="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/train_val_loss.png">
        <img src="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/train_val_loss.png" alt="Training Loss và Validation Loss của mô hình">
      </a>
      <br>
      <strong>Hình 3:</strong> Training Loss và Validation Loss của mô hình
    </td>
  </tr>
</table>

Tiếp theo là về kết quả đánh giá chất lượng mô hình dịch thuật:

<table>
  <thead>
    <tr>
      <th style="text-align: center; min-width: 120px;">Chỉ số</th>
      <th style="text-align: center; min-width: 80px;">Điểm số</th>
      <th style="text-align: center;">Đánh giá</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center"><strong>BLEU</strong></td>
      <td align="center">0.2557</td>
      <td>Bản dịch đạt mức chấp nhận được, mô hình dịch đúng ý chính nhưng chưa trùng khớp cao về hình thức câu.</td>
    </tr>
    <tr>
      <td align="center"><strong>ROUGE-1</strong></td>
      <td align="center">0.6366</td>
      <td>Giá trị cao, mô hình nắm tốt từ vựng quan trọng và bảo toàn nội dung chính của câu dịch.</td>
    </tr>
    <tr>
      <td align="center"><strong>ROUGE-2</strong></td>
      <td align="center">0.3897</td>
      <td>Mô hình tạo được nhiều cụm từ hợp lý, dù cấu trúc câu vẫn còn khác so với tham chiếu.</td>
    </tr>
    <tr>
      <td align="center"><strong>ROUGE-L</strong></td>
      <td align="center">0.5534</td>
      <td>Khả năng giữ mạch nội dung khá tốt, bản dịch nhìn chung liền mạch và dễ hiểu.</td>
    </tr>
    <tr>
      <td align="center"><strong>ROUGE-Lsum</strong></td>
      <td align="center">0.5533</td>
      <td>Chất lượng dịch ổn định trên toàn câu, ít lỗi lặp và không làm sai lệch ý nghĩa tổng thể.</td>
    </tr>
  </tbody>
</table>

> [!NOTE]
> Mô hình khi thực nghiệm trên những câu nói phức tạp thì kết quả dịch thuật chưa được như mong muốn.

Cuối cùng là kết quả nhận được trên giao diện Web App:

<details>
  <summary><strong>Demo (Ảnh chụp màn hình)</strong></summary>
  
  <br>
  
  <p align="center">
    <a href="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/initial_interface.png" target="_blank">
      <img src="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/initial_interface.png" 
           alt="Giao diện ban đầu của dự án" width="700">
    </a>
  </p>
  <p align="center"><strong>Hình 4:</strong> Giao diện ban đầu của dự án</p>

<br><br>

  <p align="center">
    <a href="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/result_interface.png" target="_blank">
      <img src="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/result_interface.png" 
           alt="Kết quả thực nghiệm trên giao diện của dự án" width="700">
    </a>
  </p>
  <p align="center"><strong>Hình 5:</strong> Kết quả thực nghiệm trên giao diện của dự án</p>

<br><br>

  <p align="center">
    <a href="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/detail_interface.png" target="_blank">
      <img src="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/detail_interface.png" 
           alt="Thông tin chi tiết về lịch sử dịch thuật" width="700">
    </a>
  </p>
  <p align="center"><strong>Hình 6:</strong> Thông tin chi tiết về lịch sử dịch thuật</p>

</details>

<div align="right">
  <a href="#readme-top">↑ Quay lại đầu trang</a>
</div>

## Công nghệ tiêu biểu

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Hugging Face Transformers](https://img.shields.io/badge/Hugging_Face_Transformers-0A66C2?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/docs/transformers/index)
[![PEFT](https://img.shields.io/badge/PEFT-0A66C2?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/docs/peft/index)

<div align="right">
  <a href="#readme-top">↑ Quay lại đầu trang</a>
</div>

## Cấu trúc mã nguồn

**Translation-App/**<br>
├── **[backend](backend/)** (Chứa mã nguồn của Backend Flask)<br>
├── **[model](model/)** (Chứa mô hình được đóng gói)<br>
├── **[notebook](notebook/)** (Chứa các Notebook trực quan hóa dữ liệu và huấn luyện mô hình)<br>
└── **[picture](picture/)** (Chứa danh mục hình ảnh)<br>

<div align="right">
  <a href="#readme-top">↑ Quay lại đầu trang</a>
</div>

## Khởi động dự án

<details>
<summary><strong>1. Tải Repository về máy</strong></summary>
<br>

Mở PowerShell hoặc Terminal rồi chạy:

```powershell
git clone https://github.com/baxflux/Translation-App.git
cd Translation-App
```

</details>

<details>
<summary><strong>2. Chuẩn bị môi trường và cài đặt thư viện</strong></summary>
<br>

Sử dụng Python 3.12+.

Tạo và kích hoạt môi trường ảo trong thư mục `backend`, rồi cài đặt các thư viện cần thiết.

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

</details>

<details>
<summary><strong>3. Truy cập hệ thống Web App</strong></summary>
<br>

Từ thư mục `backend`, chạy:

```powershell
python run.py
```

Sau khi Server Flask khởi động, mở trình duyệt và truy cập:

```text
http://127.0.0.1:5000
```

</details>

<div align="right">
  <a href="#readme-top">↑ Quay lại đầu trang</a>
</div>

## Giấy phép

Dự án này được phát hành dưới giấy phép **MIT License**.

Xem toàn bộ nội dung giấy phép tại [LICENSE](LICENSE).

<div align="right">
  <a href="#readme-top">↑ Quay lại đầu trang</a>
</div>
