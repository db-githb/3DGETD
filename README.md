<h1 align="center">3D GET-D:</h1>
<h1 align="center">3D Gaussian Editor for Test Data</h1>



**3D GET-D** is a tool designed to create cameras and 3D gaussians for testing the forward/rendering pass of 3D Gaussian Splatting applications in Nerfstudio.

---

## 🚀 **Features**

**Flexible Camera Configuration**: Easily define and adjust the number of cameras, along with their position and rotation parameters.

**Customizable 3D Gaussians**: Configure the number of 3D Gaussians and customize their base color, position, rotation, and scale for precise control over the 3D scene.

---

## 🔧  **Installation Overview**

This tool provides precompiled executables for quick and easy use on major platforms, as well as the option to clone and install the repository locally for customization or development. Detailed instructions for both approaches are provided below.

### ⚙️  **Quick Start with Executables**

For users who want a quick way to generate synthetic data without setting up the full environment, precompiled executables are provided for Linux and Windows:

- **Linux** 
- **Windows**

### 🛠️ **Cloning and Installing Repository**

#### 📋 **Prerequisites**
This tool requires **Python** and the following packages:

- **NumPy**
- **Pillow**
- **PyQt**
- **PyTorch** (CUDA enabled)

The tool has been tested with Python 3.12 and CUDA 12.1. If you're using different versions of Python or CUDA, please ensure that all required packages are compatible with your environment.

#### 📝 **Steps to Set Up**

1. **Clone the repository**:
 
        git clone https://github.com/db-githb/3DGETD.git

2. **Create environment and install dependencies**:

   Choose one of the following methods, depending on your preference for `conda` or `pip`:

   - **Using** `conda`:
        ```
        cd 3DGET
        conda env create -f environment.yml
        ```
   - **Using** `pip`
        ```
        cd 3DGETD
        pip install requirements.txt
        ```

3. **Run the tool**:

        python 3dgetd.py

## 📖 **Usage**

The project requires a specific directory structure with data and models subdirectories to organize 3D Gaussians, camera data, and Nerfstudio-compatible files. These directories, along with necessary files, are automatically created by the tool if they do not already exist.

### 📂 **Directory Structure**

The generation of 3D Gaussians and the scene's respective cameras requires a ```data``` and ```models``` subdirectory under your project directory:

```
<your-project-name>/
├─ data/
├─ models/
```
If these subdirectories do not exist, you will be prompted to create them.

In addition, Nerfstudio requires the following directory structure and names:

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
## 🎯 **Future Plans**
- Extend this project to support the 3D Gaussian Splatting framework from Inria.

---

## 🌟 **Contributions and feedback are highly encouraged!**
Feel free to submit pull requests or open issues for feature requests and bug reports.

## 📜 **Citation**

If you found this tool useful in your research, please cite it!

```bibtex
@misc{3DGETD,
  author = {Bowness, Damian},
  title = {3D GET-D: 3D Gaussian Editor for Test Data},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/db-githb/3D_GET-D},
}
```
---
## 📜 **License**
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).