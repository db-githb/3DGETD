<h1 align="center">3D GET-D:</h1>
<h1 align="center">3D Gaussian Editor for Test Data</h1>



**3D GET-D** is a tool designed to create cameras and 3D gaussians for testing the forward/rendering pass of 3D Gaussian Splatting applications in Nerfstudio.

---

## 🚀 **Features**

**Flexible Camera Configuration**: Easily define and adjust the number of cameras, along with their position and rotation parameters.

**Customizable 3D Gaussians**: Configure the number of 3D Gaussians and customize their base color, position, rotation, and scale for precise control over the 3D scene.

---

## 🔧  **Installation Overview**

This project includes shell scripts to automate the creation and setup of the required virtual environment using Conda. These scripts ensure compatibility with the installed CUDA version and use Python 3.12 as the base interpreter.
#### 📋 **Prerequisites**
Before cloning and installing the repository, please ensure the following are installed and available in your system's `PATH`:
- **Conda**: For environment creation and package management.
- **CUDA Toolkit**: Required for installing compatible `pytorch-cuda`.

The tool has been tested with Python 3.12, 3.10 and CUDA 12.1, 11.8. If you're using different versions of Python or CUDA, please ensure that all required packages are compatible with your environment.

1. **Clone the repository**:
    ```git
    git clone https://github.com/db-githb/3DGETD.git
    ```
2. **Navigate to `setup_scripts`**
    ```bash
    cd setup_scripts
    ```
3. **Make the script executable**:
    ```bash
    chmod +x conda_setup_linux.sh
    ```
4. **Run the script**

    - Conda+Linux
        ```bash
        ./conda_setup_linux.sh
        ```
    - Pip+Linux
        ```bash
        ./conda_setup_linux.sh
        ```
5. **Run the tool**:
    ```
    python 3dgetd.py
    ````
---

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