<a id="readme-top"></a>

<h1 align="center">Translation App</h1>

<h4 align="center" style="color: #555">
  An application for translating from English to Vietnamese
</h4>

<div align="center">
  <strong>English</strong> 
  •
  <a href="README.vi.md"><strong>Vietnamese</strong></a>
</div>

<br>

## Table of Contents

- [Overview](#overview)
- [Dataset](#dataset)
- [Results](#results)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [License](#license)

## Overview

This is a project to build a **Web App for one-way text translation from English to Vietnamese**, based on the large language model **Qwen2.5-0.5B**, fine-tuned on an English-Vietnamese bilingual dataset using techniques to optimize resources.

Below is a summary of the entire project development process:

<div align="center">
  <a href="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/translation_app.png" target="_blank">
    <img src="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/translation_app.png"
         alt="Overall architecture of the Translation App project" width="700">
  </a>
</div>

<p align="center">
  <strong>Figure 1:</strong> Overall architecture of the Translation App project
</p>

The first step of the project is **Exploratory Data Analysis (EDA)** on the bilingual dataset. This process takes place on the **Kaggle** platform (a website providing large amounts of free GPU), which draws important conclusions about the distribution of the length of bilingual text pairs.

Next is the model building step, which also takes place on Kaggle. Although the dataset is pre-split from Hugging Face, we only take a small portion due to resource constraints, with Train/Validation/Test distribution corresponding to **25000/2000/2000 data samples**. We then proceed to filter data by token length so that the model can learn efficiently:

1. English sentences have length in the range **(5, 40)** tokens
2. Vietnamese sentences have length in the range **(5, 50)** tokens

After that, we adjust the **Prompt** to match the structure of the Qwen model, as well as build **Tokenization** for the Train and Validation sets to ensure data consistency during training. The next step is to load the **Qwen2.5-0.5B** base model, combined with configuring the **LoRA (Low-Rank Adaptation)** technique to better fine-tune the model. This technique allows:

1. Reducing the number of parameters that need to be trained.
2. Saving GPU memory.
3. Suitable for training environments with limited resources.

After this step, we move to the stage of configuring training parameters using the **TrainingArguments** library and training with **SFTTrainer**. Throughout the training process, **Log** segments are recorded to evaluate the model with various charts (Accuracy/Loss). Additionally, we also use metrics such as **BLEU** and **ROUGE** when evaluating on the Test dataset to see the model's generalization ability and translation quality.

For testing with new data (Inference), we input a basic English sentence. We proceed to reload the base model and the newly fine-tuned model, then apply the Prompt and Tokenizer that were built previously to see the corresponding Vietnamese translation. The end of the training process is packaging the model into a Zip file for easy downloading.

The second step is to load the packaged model into the Web App part built with **Flask** Backend, combined with a simple **HTML** interface. When interacting on the browser, we input English text and the result is the translated Vietnamese text.

<div align="right">
  <a href="#readme-top">↑ Back to top</a>
</div>

## Dataset

[![Dataset](https://img.shields.io/badge/Dataset-0A66C2?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/datasets/ncduy/mt-en-vi)

The dataset for this project is called **mt-en-vi**, a bilingual English-Vietnamese dataset containing parallel bilingual texts synthesized from various English-Vietnamese sources. The dataset is located on the Hugging Face website, a platform for storing well-known and reputable datasets and models.

**Dataset Description:** Contains parallel sentence pairs between English and Vietnamese, with three main attributes:

1. **en:** Text sentence in English.
2. **vi:** Text sentence in Vietnamese.
3. **source:** Source of the bilingual sentence pair (OpenSubtitles v2018, TED2020 v1, QED v2.0a, WikiMatrix v1, wikimedia v20210402, vietnamsongngu.com, baosongngu.net, Tatoeba v2021-07-22)

This dataset has been pre-split on Hugging Face into three sets: **Train/Validation/Test**, so there is no need to re-split the data during use.

<div align="right">
  <a href="#readme-top">↑ Back to top</a>
</div>

## Results

First are some visualizations about the model training process:

<table>
  <tr>
    <td style="width: 47%; padding: 8px; text-align: center; vertical-align: bottom;">
      <a href="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/token_accuracy.png" target="_blank">
        <img src="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/token_accuracy.png" 
             alt="Token Accuracy of the model">
      </a>
      <p style="margin-top: 10px;"><strong>Figure 2:</strong> Token Accuracy of the model</p>
    </td>
    <td style="width: 53%; padding: 8px; text-align: center; vertical-align: bottom;">
      <a href="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/train_val_loss.png" target="_blank">
        <img src="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/train_val_loss.png" 
             alt="Training Loss and Validation Loss of the model">
      </a>
      <p style="margin-top: 10px;"><strong>Figure 3:</strong> Training Loss and Validation Loss of the model</p>
    </td>
  </tr>
</table>

Next are the results of evaluating the translation quality of the model:

<table>
  <thead>
    <tr>
      <th style="text-align: center; min-width: 120px;">Metric</th>
      <th style="text-align: center; min-width: 80px;">Score</th>
      <th style="text-align: center;">Assessment</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center; white-space: nowrap;"><strong>BLEU</strong></td>
      <td style="text-align: center;">0.2557</td>
      <td>Translation is acceptable, the model translates the main idea correctly but does not match well in sentence form.</td>
    </tr>
    <tr>
      <td style="text-align: center; white-space: nowrap;"><strong>ROUGE-1</strong></td>
      <td style="text-align: center;">0.6366</td>
      <td>High value, the model grasps important vocabulary well and preserves the main content of the translated sentence.</td>
    </tr>
    <tr>
      <td style="text-align: center; white-space: nowrap;"><strong>ROUGE-2</strong></td>
      <td style="text-align: center;">0.3897</td>
      <td>The model creates many reasonable phrases, although the sentence structure is still different from the reference.</td>
    </tr>
    <tr>
      <td style="text-align: center; white-space: nowrap;"><strong>ROUGE-L</strong></td>
      <td style="text-align: center;">0.5534</td>
      <td>Good ability to maintain content flow, translations are generally coherent and easy to understand.</td>
    </tr>
    <tr>
      <td style="text-align: center; white-space: nowrap;"><strong>ROUGE-Lsum</strong></td>
      <td style="text-align: center;">0.5533</td>
      <td>Stable translation quality throughout the sentence, few repetitions and does not distort the overall meaning.</td>
    </tr>
  </tbody>
</table>

<div style="border-left: 5px solid #1e88e5; padding: 16px 20px; margin: 20px 0; border-radius: 6px; background-color: #f0f7ff;">
  <p><strong style="color: #1e88e5">Note:</strong></p>
  <p>
    When testing the model on complex sentences, the translation results are not as expected.
  </p>
</div>

Finally, the results obtained on the Web App interface:

<details>
  <summary><strong> Demo (Screenshot) </strong></summary>
  
  <br>
  
  <p align="center">
    <a href="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/initial_interface.png" target="_blank">
      <img src="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/initial_interface.png" 
           alt="Initial interface of the project" width="700">
    </a>
  </p>
  <p align="center"><strong>Figure 4:</strong> Initial interface of the project</p>

<br><br>

  <p align="center">
    <a href="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/result_interface.png" target="_blank">
      <img src="https://raw.githubusercontent.com/baxflux/Translation-App/main/picture/result_interface.png" 
           alt="Test results on the project interface" width="700">
    </a>
  </p>
  <p align="center"><strong>Figure 5:</strong> Test results on the project interface</p>

</details>

<div align="right">
  <a href="#readme-top">↑ Back to top</a>
</div>

## Tech Stack

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Hugging Face Transformers](https://img.shields.io/badge/Hugging_Face_Transformers-0A66C2?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/docs/transformers/index)
[![PEFT](https://img.shields.io/badge/PEFT-0A66C2?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/docs/peft/index)

<div align="right">
  <a href="#readme-top">↑ Back to top</a>
</div>

## Project Structure

**Translation-App/**<br>
├── **[backend](backend/)** (Contains Flask Backend source code)<br>
├── **[model](model/)** (Contains packaged model)<br>
├── **[notebook](notebook/)** (Contains notebooks for data visualization and model training)<br>
└── **[picture](picture/)** (Contains image directory)<br>

<div align="right">
  <a href="#readme-top">↑ Back to top</a>
</div>

## Getting Started

<details>
<summary><strong>1. Clone the Repository</strong></summary>
<br>

Open PowerShell or Terminal and run:

```powershell
git clone https://github.com/baxflux/Translation-App.git
cd Translation-App
```

</details>

<details>
<summary><strong>2. Prepare the Environment and Install Libraries</strong></summary>
<br>

Use Python 3.12+.

Create and activate a virtual environment in the `backend` directory, then install the required libraries.

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

</details>

<details>
<summary><strong>3. Access the Web App System</strong></summary>
<br>

From the `backend` directory, run:

```powershell
python run.py
```

After Flask Server starts, open your browser and visit:

```text
http://127.0.0.1:5000
```

</details>

<div align="right">
  <a href="#readme-top">↑ Back to top</a>
</div>

## License

This project is released under the **MIT License**.

See the full license content at [LICENSE](LICENSE).

<div align="right">
  <a href="#readme-top">↑ Back to top</a>
</div>
