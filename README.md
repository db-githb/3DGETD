<h1 align="center">3D GET-D:</h1>
<h1 align="center">3D Gaussian Editor for Test Data</h1>

![gaussian](readme_images/3dgetd_demo.png)

**3D GET-D** is a tool designed to create cameras and 3D gaussians for testing the forward/rendering pass of 3D Gaussian Splatting applications in Nerfstudio.

---

## 🚀 **Features**

**Flexible Camera Configuration**: Easily define and adjust the number of cameras, along with their position and rotation parameters.

**Customizable 3D Gaussians**: Configure the number of 3D Gaussians and customize their base color, position, rotation, and scale for precise control over the 3D scene.

![features](readme_images/features.png)

---

## 🔧  **Installation Overview**

This project includes shell scripts to automate the creation and setup of the required virtual environment using Conda. These scripts ensure compatibility with the installed Python version, CUDA version and PyTorch version.
#### 📋 **Prerequisites**
Before cloning and installing the repository, please ensure the following are installed and available in your system's `PATH`:
- **Conda**: For environment creation and package management.
- **CUDA Toolkit**: Required for installing compatible `pytorch-cuda`.

The tool has been tested with Python 3.12, 3.10 and CUDA 12.1, 11.8. If you're using different versions of Python or CUDA, please ensure that all required packages are compatible with your environment.

**Windows Users**: All the steps in the following guide must be run inside a `bash` shell (e.g. Git Bash, WSL, or another Bash environment).  If using Conda, ensure that Conda is added to the PATH variable. Alternatively, use the Anaconda Terminal for setup to avoid PATH configuration issues.

**Linux Users**: You can run the commands directly in your terminal.

#### 📝 **Steps to Set Up Environment**

1. **Clone the repository**:
    ```git
    git clone https://github.com/db-githb/3DGETD.git
    ```
2. **Make setup_script.sh executable**:
    ```bash
    chmod +x setup_script.sh
    ```
3. **Run `setup_3dgetd.sh`**
    ```bash
    ./setup_script.sh
    ```
    The script will prompt you to choose your package manager, `pip` or `conda`.
#### ▶️ **Run the tool**:

Once the environment is set up, run the tool using the following command:

    ./run_3dgetd.sh
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
- Create executables
- Extend this project to support the 3D Gaussian Splatting framework from Inria.

---

## 🌟 **Contributions and feedback are highly encouraged!**
Feel free to submit pull requests or open issues for feature requests and bug reports.

---
## 📜 **License**
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).