<div style="text-align: center;">
  <h1 style="margin: 0; font-size: 24px;">3D GET-D</h1>
  <h2 style="font-size: 24px; margin-top: 8px;">3D Gaussian Editor for Test Data</h2>
</div>


**3D GET-D** is a tool designed to create cameras and 3D gaussians for testing the forward/rendering pass of 3D Gaussian Splatting applications in Nerfstudio.

---

## 🚀 Features

**Flexible Camera Configuration**: Easily define and adjust the number of cameras, along with their position and rotation parameters.

**Customizable 3D Gaussians**: Configure the number of 3D Gaussians and customize their base color, position, rotation, and scale for precise control over the 3D scene.

---

## 🔧 Installation

This tool provides precompiled executables for quick and easy use on major platforms, as well as the option to clone and install the repository locally for customization or development. Choose the method that best fits your needs! Detailed instructions for both approaches are provided below.

### ⚙️ Executables

For users who want a quick way to generate synthetic data without setting up the full environment, precompiled executables are provided for Linux and Windows:

- **Linux** 
- **Windows**

### 🛠️ Cloning and Installing Repo

#### Prerequisites

#### Steps

1. Clone the repository:

2. Install dependencies:

3. Run the tool:

## 📖 Usage

### 📂 Directory Structure

The generation of 3D Gaussians and the scene's respective cameras requires a data and models subdirectory underneath your project directory:

```
<your-project-name>/
├─ data/
├─ models/
```
If these subdirectories do not exist, you will be prompted to create them.

In addition, Nerfstudio requires the following directory structure:

```
<your-project-name>/
├─ data/
│  ├─ <your-cameras-name>/
│  │  ├─ images/
│  │  │  ├─ test.jpg
│  │  ├─ cameras.txt
│  │  ├─ images.txt
├─ models/
│  ├─ <your-experiment-name>/
│  │  ├─ splatfacto/
│  │  │  ├─ checkpoint-0000000.ckpt
│  │  ├─ config.yml
│  │  ├─ dataparsers_transform.json
```

These required subdirectories and files are created by the tool. 

---
## 📜 License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## 🎯 Future Plans
- Extend this project to support the 3D Gaussian Splatting framework from Inria.

---

## 🌟 Contributions and feedback are highly encouraged!
Feel free to submit pull requests or open issues for feature requests and bug reports.