<p align="center">

  <h1 align="center"> 3D Gaussian Generator</h1>
</p>

**3D Gaussian Generator** is a tool designed to create cameras and 3D gaussians for testing the forward/rendering pass of 3D Gaussian Splatting applications in Nerfstudio.

---

## 🚀 Features

**Flexible Camera Configuration**: Easily define and adjust the number of cameras, along with their position and rotation parameters, to fit your setup.

**Customizable 3D Gaussians**: Configure the number of 3D Gaussians and customize their base color, position, rotation, and scale for precise control over the 3D scene.

---

## 🔧 Installation

This project provides precompiled executables for quick and easy use on major platforms, as well as the option to clone and install the repository locally for customization or development. Choose the method that best fits your needs! Detailed instructions for both approaches are provided below.

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

The generation of 3D Gaussians requires a data and models subdirectory underneath your project directory:

```
<your-project>/
├─ <data>/
├─ <models>/
```
If these subdirectories do not exist, you will be prompted to create them.

---
## 📜 License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## 🎯 Future Plans
- Extend this project to support the 3D Gaussian Splatting framework from Inria.

---

## 🌟 Contributions and feedback are highly encouraged!
Feel free to submit pull requests or open issues for feature requests and bug reports.