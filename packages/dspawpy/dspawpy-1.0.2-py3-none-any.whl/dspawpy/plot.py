# -*- coding: utf-8 -*-
import json
import os

import h5py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from dspawpy.io.read import load_h5
from scipy.interpolate import interp1d


def average_along_axis(
    datafile="potential.h5",
    task: str = "potential",
    axis=2,
    smooth=False,
    smooth_frac=0.8,
    raw=False,
    subtype: str = None,
    **kwargs,
):
    r"""绘制沿着某个轴向的物理量平均值曲线

    Parameters
    ----------
    datafile : str or list or np.ndarray
        h5或json文件路径或包含任意这些文件的文件夹，默认 'potential.h5'
    task: str
        任务类型，可以是 'rho', 'potential', 'elf', 'pcharge', 'rhoBound'
    axis : int
        沿着哪个轴向绘制势能曲线, 默认2
    smooth : bool
        是否平滑, 默认False
    smooth_frac : float
        平滑系数, 默认0.8
    raw : bool
        是否返回绘图数据到csv文件
    subtype : str
        用于指定task数据子类，暂时只支持 TotalLocalPotential，默认None，代表绘制 TotalElectrostaticPotential
    **kwargs : dict
        其他参数, 传递给 matplotlib.pyplot.plot

    Returns
    -------
    axes: matplotlib.axes._subplots.AxesSubplot
        可传递给其他函数进行进一步处理

    Examples
    --------
    >>> from dspawpy.plot import average_along_axis

    读取 potential.h5 文件中的数据，绘图并保存原始绘图数据到csv文件

    >>> average_along_axis(datafile='/data/home/hzw1002/dspawpy_repo/test/2.7/potential.h5', task='potential', axis=2, smooth=True, smooth_frac=0.8, raw=True)
    <module 'matplotlib.pyplot' from '/data/home/hzw1002/anaconda3/lib/python3.9/site-packages/matplotlib/pyplot.py'>
    """
    assert task in [
        "rho",
        "potential",
        "elf",
        "pcharge",
        "rhoBound",
    ], "仅支持 rho, potential, elf, pcharge, rhoBound 任务类型"
    if subtype is not None:
        assert (
            task == "potential" and subtype == "TotalLocalPotential"
        ), '目前仅支持"potential"的"TotalLocalPotential"子类'

    # only for compatibility
    if isinstance(datafile, list) or isinstance(datafile, np.ndarray):
        ys = datafile  # expect np.ndarray or list

    # search datafile in the given directory
    elif os.path.isdir(datafile):
        directory = datafile  # specified datafile is actually a directory
        print("您指定了一个文件夹，正在查找相关h5或json文件...")
        if os.path.exists(os.path.join(directory, f"{task}.h5")):
            datafile = os.path.join(directory, f"{task}.h5")
            print("Readingf {task}.h5...")
        elif os.path.exists(os.path.join(directory, f"{task}.json")):
            datafile = os.path.join(directory, f"{task}.json")
            print("Readingf {task}.json...")
        else:
            raise FileNotFoundError(f"未找到{task}.h5/{task}.json文件！")

    # parse the real datafile
    elif datafile.endswith(".h5"):
        hfile = datafile
        hdict = load_h5(hfile)
        grid = hdict["/AtomInfo/Grid"]

        if task == "rho":
            if subtype is None:
                _key = "/Rho/TotalCharge"
            else:
                _key = f"/Rho/{subtype}"
        elif task == "potential":
            if subtype is None:
                _key = "/Potential/TotalElectrostaticPotential"
            elif subtype == "TotalLocalPotential":
                _key = f"/Potential/{subtype}"
        elif task == "elf":
            if subtype is None:
                _key = "/ELF/TotalELF"
            else:
                _key = f"/ELF/{subtype}"
        elif task == "pcharge":
            if subtype is None:
                _key = "/Pcharge/1/TotalCharge"
            else:
                _key = f"/Pcharge/1/{subtype}"
        elif task == "rhoBound":
            if subtype is None:
                _key = "/Rho"
            else:
                _key = subtype

        if _key not in hdict:
            raise KeyError(f"未找到{_key}键！")

        # DS-PAW 数据写入h5 列优先
        # h5py 从h5读取数据 默认行优先
        # np.array(data_list) 默认行优先
        # 所以这里先以 行优先 把 “h5 行优先 读进来的数据” 转成一维， 再以 列优先 转成 grid 对应的维度
        tmp_pot = np.asarray(hdict[_key]).reshape([-1, 1], order="C")
        ys = tmp_pot.reshape(grid, order="F")

    elif datafile.endswith(".json"):
        jfile = datafile
        with open(jfile, "r") as f:
            jdict = json.load(f)
        grid = jdict["AtomInfo"]["Grid"]

        if task == "rho":
            if subtype is None:
                ys = np.asarray(jdict["Rho"]["TotalCharge"]).reshape(grid, order="F")
            else:
                ys = np.asarray(jdict["Rho"][subtype]).reshape(grid, order="F")
        elif task == "potential":
            if subtype is None:
                ys = np.asarray(
                    jdict["Potential"]["TotalElectrostaticPotential"]
                ).reshape(grid, order="F")
            else:
                ys = np.asarray(jdict["Potential"][subtype]).reshape(grid, order="F")
        elif task == "elf":
            if subtype is None:
                ys = np.asarray(jdict["ELF"]["TotalELF"]).reshape(grid, order="F")
            else:
                ys = np.asarray(jdict["ELF"][subtype]).reshape(grid, order="F")
        elif task == "pcharge":
            if subtype is None:
                ys = np.asarray(jdict["Pcharge"][0]["TotalCharge"]).reshape(
                    grid, order="F"
                )
            else:
                ys = np.asarray(jdict["Pcharge"][0][subtype]).reshape(grid, order="F")
        else:
            if subtype is None:
                ys = np.asarray(jdict["Rho"]).reshape(grid, order="F")
            else:
                ys = np.asarray(jdict[subtype]).reshape(grid, order="F")

    else:
        raise TypeError("仅支持读取h5或json文件或直接传入数组！")

    all_axis = [0, 1, 2]
    all_axis.remove(axis)
    y = np.mean(ys, tuple(all_axis))
    x = np.arange(len(y))

    if raw:
        pd.DataFrame({"x": x, "y": y}).to_csv(f"raw{task}_axis{axis}.csv", index=False)
    if smooth:
        s = sm.nonparametric.lowess(y, x, frac=smooth_frac)
        if raw:
            pd.DataFrame({"x": s[:, 0], "y": s[:, 1]}).to_csv(
                f"raw{task}_axis{axis}_smooth.csv", index=False
            )

        plt.plot(s[:, 0], s[:, 1], label="macroscopic average", **kwargs)

    plt.plot(x, y, **kwargs)

    return plt


def plot_aimd(
    datafile: str = "aimd.h5",
    show: bool = True,
    figname: str = "aimd.png",
    flags_str="12345",
    raw=False,
):
    r"""AIMD任务完成后，绘制关键物理量的收敛过程图

    aimd.h5 -> aimd.png

    Parameters
    ----------
    datafile : str or list
        h5文件位置. 例如 'aimd.h5' 或 ['aimd.h5', 'aimd2.h5']
    show : bool
        是否展示交互界面. 默认 False
    figname : str
        保存的图片路径. 默认 'aimd.h5'
    flags_str : str
        子图编号.
        1. 动能
        2. 总能
        3. 压力
        4. 温度
        5. 体积
    raw : bool
        是否输出绘图数据到csv文件

    Returns
    ----------
    figname : str
        图片路径，默认 'aimd.png'

    Examples
    ----------
    >>> from dspawpy.plot import plot_aimd

    读取 aimd.h5 文件内容，画出动能、总能、温度、体积的收敛过程图，并保存相应数据到 rawaimd_*.csv 中

    >>> plot_aimd(datafile='/data/home/hzw1002/dspawpy_repo/test/2.18/aimd.h5', flags_str='1245', raw=False, show=False, figname=None)
    正在处理子图1
     reading /data/home/hzw1002/dspawpy_repo/test/2.18/aimd.h5...
    正在处理子图2
     reading /data/home/hzw1002/dspawpy_repo/test/2.18/aimd.h5...
    正在处理子图4
     reading /data/home/hzw1002/dspawpy_repo/test/2.18/aimd.h5...
    正在处理子图5
     reading /data/home/hzw1002/dspawpy_repo/test/2.18/aimd.h5...
    """
    # 处理用户读取，按顺序去重
    temp = set()
    flags = [x for x in flags_str if x not in temp and (temp.add(x) or True)]
    if " " in flags:  # remove space
        flags.remove(" ")

    for flag in flags:
        assert flag in ["1", "2", "3", "4", "5"], "读取错误！"

    # 开始画组合图
    N_figs = len(flags)
    fig, axes = plt.subplots(N_figs, 1, sharex=True, figsize=(6, 2 * N_figs))
    if N_figs == 1:  # 'AxesSubplot' object is not subscriptable
        axes = [axes]  # 避免上述类型错误
    fig.suptitle("DSPAW AIMD")
    for i, flag in enumerate(flags):
        print("正在处理子图" + flag)
        # 读取数据
        xs, ys = _read_aimd_converge_data(datafile, flag)
        if raw:
            pd.DataFrame({"x": xs, "y": ys}).to_csv(f"rawaimd_{flag}.csv", index=False)

        axes[i].plot(xs, ys)  # 绘制坐标点
        # 子图的y轴标签
        if flag == "1":
            axes[i].set_ylabel("Kinetic Energy (eV)")
        elif flag == "2":
            axes[i].set_ylabel("Energy (eV)")
        elif flag == "3":
            axes[i].set_ylabel("Pressure Kinetic (kbar)")
        elif flag == "4":
            axes[i].set_ylabel("Temperature (K)")
        else:
            axes[i].set_ylabel("Volume (Angstrom^3)")

    plt.tight_layout()
    # save and show
    if figname:
        os.makedirs(os.path.dirname(os.path.abspath(figname)), exist_ok=True)
        plt.savefig(figname, dpi=300)
        print(f"--> 图片已保存为 {os.path.abspath(figname)}")
    if show:
        plt.show()


def plot_bandunfolding(
    datafile: str = "band.h5", ef=0.0, de=0.05, dele=0.06, raw=False
):
    r"""能带反折叠任务完成后，读取 h5 或 json 文件数据绘图

    band.h5/band.json -> bandunfolding.png

    Parameters
    ----------
    datafile : str
        h5或json文件路径或包含任意这些文件的文件夹，默认 'band.h5'
    ef : float
        费米能级，默认置于 y = 0 处
    de : float
        能带宽度，默认0.05
    dele : float
        能带间隔，默认0.06
    raw : bool
        是否输出绘图数据到rawbandunfolding.csv

    Returns
    -------
    axes: matplotlib.axes._subplots.AxesSubplot
        可传递给其他函数进行进一步处理

    Examples
    --------

    绘图并保存绘图数据到rawbandunfolding.csv

    >>> from dspawpy.plot import plot_bandunfolding
    >>> plot_bandunfolding("/data/home/hzw1002/dspawpy_repo/test/2.22/band.h5", raw=True)
    Reading /data/home/hzw1002/dspawpy_repo/test/2.22/band.h5...
    <module 'matplotlib.pyplot' from '/data/home/hzw1002/anaconda3/lib/python3.9/site-packages/matplotlib/pyplot.py'>
    """
    # search datafile in the given directory
    if os.path.isdir(datafile):
        directory = datafile  # specified datafile is actually a directory
        print("您指定了一个文件夹，正在查找相关h5或json文件...")
        if os.path.exists(os.path.join(directory, "band.h5")):
            datafile = os.path.join(directory, "band.h5")
            print("Reading band.h5...")
        elif os.path.exists(os.path.join(directory, "band.json")):
            datafile = os.path.join(directory, "band.json")
            print("Reading band.json...")
        else:
            raise FileNotFoundError("未找到band.h5/band.json文件！")

    if datafile.endswith(".h5"):
        # band = load_h5(datafile)
        import h5py

        print(f"Reading {os.path.abspath(datafile)}...")
        f = h5py.File(datafile, "r")
        number_of_band = np.array(f["/BandInfo/NumberOfBand"])[0]
        # number_of_band = band["/BandInfo/NumberOfBand"][0]
        number_of_kpoints = np.array(f["/BandInfo/NumberOfKpoints"])[0]
        # number_of_kpoints = band["/BandInfo/NumberOfKpoints"][0]
        data = np.array(f["/UnfoldingBandInfo/Spin1/UnfoldingBand"])
        # data = band["/UnfoldingBandInfo/Spin1/UnfoldingBand"]
        weight = np.array(f["/UnfoldingBandInfo/Spin1/Weight"])
        # weight = band["/UnfoldingBandInfo/Spin1/Weight"]
    elif datafile.endswith(".json"):
        with open(datafile, "r") as f:
            band = json.load(f)
        number_of_band = band["BandInfo"]["NumberOfBand"]
        number_of_kpoints = band["BandInfo"]["NumberOfKpoints"]
        data = band["UnfoldingBandInfo"]["Spin1"]["UnfoldingBand"]
        weight = band["UnfoldingBandInfo"]["Spin1"]["Weight"]
    else:
        raise TypeError("仅支持读取h5或json文件！")

    celtot = np.array(data).reshape((number_of_kpoints, number_of_band)).T
    proj_wt = np.array(weight).reshape((number_of_kpoints, number_of_band)).T
    X2, Y2, Z2, emin = getEwtData(
        number_of_kpoints, number_of_band, celtot, proj_wt, ef, de, dele
    )

    if raw:
        pd.DataFrame({"Y": Y2, "Z": Z2}, index=X2).to_csv(
            "rawbandunfolding.csv", header=["Y", "color"], index=True, index_label="X"
        )

    plt.clf()
    plt.scatter(X2, Y2, c=Z2, cmap="hot")
    plt.xlim(0, 200)
    plt.ylim(emin - 0.5, 15)
    ax = plt.gca()
    plt.colorbar()
    ax.set_facecolor("black")

    return plt


def plot_optical(
    datafile: str = "optical.h5",
    key: str = "AbsorptionCoefficient",
    index: int = 0,
    raw=False,
):
    """光学性质计算任务完成后，读取数据并绘制预览图

    optical.h5/optical.json -> optical.png

    Parameters
    ----------
    datafile : str
        h5或json文件路径或包含任意这些文件的文件夹，默认 'optical.h5'
    key: str
        可选 "AbsorptionCoefficient", "ExtinctionCoefficient", "RefractiveIndex", "Reflectance" 中的任意一个，默认 "AbsorptionCoefficient"
    index : int
        序号，默认0
    raw : bool
        是否保存绘图数据到csv

    Returns
    -------
    axes: matplotlib.axes._subplots.AxesSubplot
        可传递给其他函数进行进一步处理

    Examples
    --------

    绘图并保存绘图数据到rawoptical.csv

    >>> from dspawpy.plot import plot_optical
    >>> plot_optical("/data/home/hzw1002/dspawpy_repo/test/2.12/scf.h5", "AbsorptionCoefficient", 0, raw=True)
    >>> plot_optical("/data/home/hzw1002/dspawpy_repo/test/2.12/optical.json", "AbsorptionCoefficient", 0, raw=True)
    """
    # search datafile in the given directory
    if os.path.isdir(datafile):
        directory = datafile  # specified datafile is actually a directory
        print("您指定了一个文件夹，正在查找相关h5或json文件...")
        if os.path.exists(os.path.join(directory, "optical.h5")):
            datafile = os.path.join(directory, "optical.h5")
            print("Reading optical.h5...")
        elif os.path.exists(os.path.join(directory, "optical.json")):
            datafile = os.path.join(directory, "optical.json")
            print("Reading optical.json...")
        else:
            raise FileNotFoundError("未找到optical.h5/optical.json文件！")

    # parse the real datafile
    if datafile.endswith("h5"):
        data_all = load_h5(datafile)
        energy = data_all["/OpticalInfo/EnergyAxe"]
        data = data_all["/OpticalInfo/" + key]
    elif datafile.endswith("json"):
        with open(datafile, "r") as fin:
            data_all = json.load(fin)
        energy = data_all["OpticalInfo"]["EnergyAxe"]
        data = data_all["OpticalInfo"][key]
    else:
        raise TypeError("仅支持读取h5或json文件！")

    data = np.asarray(data).reshape(len(energy), 6)[:, index]
    inter_f = interp1d(energy, data, kind="cubic")
    energy_spline = np.linspace(energy[0], energy[-1], 2001)
    data_spline = inter_f(energy_spline)

    if raw:
        pd.DataFrame({"energy": energy, "data": data}).to_csv(
            "rawoptical.csv", index=False
        )
        pd.DataFrame(
            {"energy_spline": energy_spline, "data_spline": data_spline}
        ).to_csv("rawoptical_spline.csv", index=False)

    plt.plot(energy_spline, data_spline, c="b")
    plt.xlabel("Photon energy (eV)")
    plt.ylabel("%s %s" % (key, r"$\alpha (\omega )(cm^{-1})$"))


def plot_phonon_thermal(
    datafile: str = "phonon.h5",
    figname: str = "phonon.png",
    show: bool = True,
    raw=False,
):
    """声子热力学计算任务完成后，绘制相关物理量随温度变化曲线

    phonon.h5/phonon.json -> phonon.png

    Parameters
    ----------
    datafile : str
        h5或json文件路径或包含任意这些文件的文件夹，默认 'phonon.h5'
    figname : str
        保存图片的文件名
    show : bool
        是否弹出交互界面
    raw : bool
        是否保存绘图数据到rawphonon.csv文件

    Returns
    ----------
    figname : str
        图片路径，默认 'phonon.png'

    Examples
    --------
    >>> from dspawpy.plot import plot_phonon_thermal
    >>> plot_phonon_thermal('/data/home/hzw1002/dspawpy_repo/test/2.26/phonon.h5', figname='/data/home/hzw1002/dspawpy_repo/test/out/phonon_thermal.png', show=False)
    Reading /data/home/hzw1002/dspawpy_repo/test/2.26/phonon.h5...
    --> 图片已保存为 /data/home/hzw1002/dspawpy_repo/test/out/phonon_thermal.png
    """
    # search datafile in the given directory
    if os.path.isdir(datafile):
        directory = datafile  # specified datafile is actually a directory
        print("您指定了一个文件夹，正在查找相关h5或json文件...")
        if os.path.exists(os.path.join(directory, "phonon.h5")):
            datafile = os.path.join(directory, "phonon.h5")
            print("Reading phonon.h5...")
        elif os.path.exists(os.path.join(directory, "phonon.json")):
            datafile = os.path.join(directory, "phonon.json")
            print("Reading phonon.json...")
        else:
            raise FileNotFoundError("未找到phonon.h5/phonon.json文件！")

    if datafile.endswith(".h5"):
        hfile = datafile
        ph = h5py.File(hfile, "r")
        print(f"Reading {hfile}...")
        if "/ThermalInfo/Temperatures" not in ph:
            raise KeyError(
                "❓ No thermal info in datafile, you probably gave a wrong phonon.h5 file"
            )
        temp = np.array(ph["/ThermalInfo/Temperatures"])
        entropy = np.array(ph["/ThermalInfo/Entropy"])
        heat_capacity = np.array(ph["/ThermalInfo/HeatCapacity"])
        helmholts_free_energy = np.array(ph["/ThermalInfo/HelmholtzFreeEnergy"])
    elif datafile.endswith(".json"):
        jfile = datafile
        with open(jfile, "r") as f:
            data = json.load(f)
        print(f"Reading {jfile}...")
        temp = np.array(data["ThermalInfo"]["Temperatures"])
        entropy = np.array(data["ThermalInfo"]["Entropy"])
        heat_capacity = np.array(data["ThermalInfo"]["HeatCapacity"])
        helmholts_free_energy = np.array(data["ThermalInfo"]["HelmholtzFreeEnergy"])
    else:
        raise TypeError("仅支持读取h5或json文件！")

    if raw:
        pd.DataFrame(
            {
                "temp": temp,
                "entropy": entropy,
                "heat_capacity": heat_capacity,
                "helmholts_free_energy": helmholts_free_energy,
            }
        ).to_csv("rawphonon.csv", index=False)

    plt.plot(temp, entropy, c="red", label="Entropy (J/K/mol)")
    plt.plot(temp, heat_capacity, c="green", label="Heat Capacity (J/K/mol)")
    plt.plot(
        temp, helmholts_free_energy, c="blue", label="Helmholtz Free Energy (kJ/mol)"
    )
    plt.xlabel("Temperature(K)")
    plt.ylabel("Thermal Properties")
    plt.tick_params(direction="in")  # 刻度线朝内
    plt.grid(alpha=0.2)
    plt.legend()
    plt.title("Thermal")

    plt.tight_layout()
    # save and show
    if figname:
        os.makedirs(os.path.dirname(os.path.abspath(figname)), exist_ok=True)
        plt.savefig(figname, dpi=300)
        print(f"--> 图片已保存为 {os.path.abspath(figname)}")
    if show:
        plt.show()


def plot_polarization_figure(
    directory: str,
    repetition: int = 2,
    annotation: bool = False,
    annotation_style: int = 1,
    show: bool = True,
    figname: str = "pol.png",
    raw=False,
):
    """绘制铁电极化结果图

    Parameters
    ----------
    directory : str
        铁电极化计算任务主目录
    repetition : int
        沿上（或下）方向重复绘制的次数, 默认 2
    annotation : bool
        是否显示首尾构型的铁电极化数值, 默认显示
    show : bool
        是否交互显示图片, 默认 True
    figname : str
        图片保存路径, 默认 'pol.png'
    raw : bool
        是否将原始数据保存到csv文件

    Returns
    -------
    axes: matplotlib.axes._subplots.AxesSubplot
        可传递给其他函数进行进一步处理

    Examples
    --------
    >>> from dspawpy.plot import plot_polarization_figure
    >>> plot_polarization_figure(directory='/data/home/hzw1002/dspawpy_repo/test/2.20', figname='/data/home/hzw1002/dspawpy_repo/test/out/pol.png', show=False)
    --> 图片已保存为 /data/home/hzw1002/dspawpy_repo/test/out/pol.png
    array([<Axes: title={'center': 'Px'}>, <Axes: title={'center': 'Py'}>,
           <Axes: title={'center': 'Pz'}>], dtype=object)
    """
    assert repetition >= 0, "重复次数必须是自然数"
    subfolders, quantum, totals = _get_subfolders_quantum_totals(directory)
    number_sfs = [int(sf) for sf in subfolders]
    fig, axes = plt.subplots(1, 3, sharey=True)
    xyz = ["x", "y", "z"]
    for j in range(3):  # x, y, z
        ys = np.empty(shape=(len(subfolders), repetition * 2 + 1))
        for r in range(repetition + 1):
            ys[:, repetition - r] = totals[:, j] - quantum[j] * r
            ys[:, repetition + r] = totals[:, j] + quantum[j] * r

        axes[j].plot(number_sfs, ys, ".")  # plot
        axes[j].set_title("P%s" % xyz[j])
        axes[j].xaxis.set_ticks(number_sfs)  # 设置x轴刻度
        axes[j].set_xticklabels(labels=subfolders, rotation=90)
        axes[j].grid(axis="x", color="gray", linestyle=":", linewidth=0.5)
        axes[j].tick_params(direction="in")
        # set y ticks using the first and last values
        if annotation:
            if annotation_style == 2:
                style = "arc,angleA=-0,angleB=0,armA=-10,armB=0,rad=0"
                for i in range(repetition * 2 + 1):
                    axes[j].annotate(
                        f"{ys[0,i]:.2f}",
                        xy=(number_sfs[0], ys[0, i]),
                        xycoords="data",
                        xytext=(number_sfs[-1] + 2, ys[0, i] - 8),
                        textcoords="data",
                        arrowprops=dict(
                            arrowstyle="->",
                            color="black",
                            linewidth=0.75,
                            shrinkA=2,
                            shrinkB=1,
                            connectionstyle=style,
                        ),
                    )
                    axes[j].annotate(
                        f"{ys[-1,i]:.2f}",
                        xy=(number_sfs[-1], ys[-1, i]),
                        xycoords="data",
                        xytext=(number_sfs[-1] + 2, ys[-1, i] + 8),
                        textcoords="data",
                        arrowprops=dict(
                            arrowstyle="->",
                            color="black",
                            linewidth=0.75,
                            shrinkA=2,
                            shrinkB=1,
                            connectionstyle=style,
                        ),
                    )
            elif annotation_style == 1:
                for i in range(repetition * 2 + 1):
                    axes[j].annotate(
                        text=f"{ys[0,i]:.2f}",
                        xy=(0, ys[0, i]),
                        xytext=(0, ys[0, i] - np.max(ys) / repetition / 5),
                    )
                    axes[j].annotate(
                        text=f"{ys[-1,i]:.2f}",
                        xy=(len(subfolders) - 1, ys[-1, i]),
                        xytext=(
                            len(subfolders) - 1,
                            ys[-1, i] - np.max(ys) / repetition / 5,
                        ),
                    )
            else:
                raise ValueError("annotation_style must be 1 or 2")

        if raw:
            pd.DataFrame(ys, index=subfolders).to_csv(f"pol_{xyz[j]}.csv")

    plt.tight_layout()
    # save and show
    if figname:
        os.makedirs(os.path.dirname(os.path.abspath(figname)), exist_ok=True)
        plt.savefig(figname, dpi=300)
        print(f"--> 图片已保存为 {os.path.abspath(figname)}")
    if show:
        plt.show()

    return axes


def _get_subfolders_quantum_totals(directory: str):
    """返回铁电极化计算任务的子目录、量子数、极化总量；

    请勿创建其他子目录，否则会被错误读取

    Parameters
    ----------
    directory：str
        铁电极化计算任务主目录

    Returns
    -------
    subfolders : list
        子目录列表
    quantum : np.ndarray
        量子数，xyz三个方向, shape=(1, 3)
    totals : np.ndarray
        极化总量，xyz三个方向, shape=(len(subfolders), 3)
    """

    raw_subfolders = next(os.walk(directory))[1]
    subfolders = []
    for subfolder in raw_subfolders:
        assert (
            0 <= int(subfolder) < 100
        ), f"--> You should rename subfolders to 0~99, but {subfolder} found"
        try:
            assert 0 <= int(subfolder) < 100
            subfolders.append(subfolder)
        except:
            pass
    subfolders.sort()  # 从小到大排序
    if os.path.exists(f"{os.path.join(directory, subfolders[0])}/scf.h5"):
        # quantum number if constant across the whole calculation,
        # so, read only once
        quantum = np.array(
            h5py.File(f"{os.path.join(directory, subfolders[0])}/scf.h5").get(
                "/PolarizationInfo/Quantum"
            )
        )
        # the Total number is not constant
        totals = np.empty(shape=(len(subfolders), 3))
        for i, fd in enumerate(subfolders):
            data = h5py.File(f"{os.path.join(directory, fd)}/scf.h5")
            total = np.array(data.get("/PolarizationInfo/Total"))
            totals[i] = total

    elif os.path.exists(f"{os.path.join(directory, subfolders[0])}/polarization.json"):
        # quantum number if constant across the whole calculation,
        # so, read only once
        with open(
            f"{os.path.join(directory, subfolders[0])}/polarization.json", "r"
        ) as f:
            quantum = json.load(f)["PolarizationInfo"]["Quantum"]
        # the Total number is not constant
        totals = np.empty(shape=(len(subfolders), 3))
        for i, fd in enumerate(subfolders):
            with open(f"{os.path.join(directory, fd)}/polarization.json", "r") as f:
                data = json.load(f)
            total = data["PolarizationInfo"]["Total"]
            totals[i] = np.array(total, dtype=float)

    else:
        raise ValueError("no polarization.json or scf.h5 file found")

    return subfolders, quantum, totals


def getEwtData(nk, nb, celtot, proj_wt, ef, de, dele):
    emin = np.min(celtot) - de
    emax = np.max(celtot) - de

    emin = np.floor(emin - 0.2)
    emax = max(np.ceil(emax) * 1.0, 5.0)

    nps = int((emax - emin) / de)

    X = np.zeros((nps + 1, nk))
    Y = np.zeros((nps + 1, nk))

    X2 = []
    Y2 = []
    Z2 = []

    for ik in range(nk):
        for ip in range(nps + 1):
            omega = ip * de + emin + ef
            X[ip][ik] = ik
            Y[ip][ik] = ip * de + emin
            ewts_value = 0
            for ib in range(nb):
                smearing = dele / np.pi / ((omega - celtot[ib][ik]) ** 2 + dele**2)
                ewts_value += smearing * proj_wt[ib][ik]
            if ewts_value > 0.01:
                X2.append(ik)
                Y2.append(ip * de + emin)
                Z2.append(ewts_value)

    Z2_half = max(Z2) / 2

    for i, x in enumerate(Z2):
        if x > Z2_half:
            Z2[i] = Z2_half

    return X2, Y2, Z2, emin


def _read_aimd_converge_data(datafile: str, index: str = None):
    """从datafile指定的路径读取index指定的数据，返回绘图用的xs和ys两个数组

    Parameters
    ----------
    datafile : str or list
        hdf5文件路径，如 'aimd.h5' 或 ['aimd.h5', 'aimd2.h5']
    index : str
        编号, 默认 None

    Returns
    -------
    xs : np.ndarray
        x轴数据
    ys : np.ndarray
        y轴数据
    """
    if isinstance(datafile, list):
        xs = []
        ys = []
        for i, df in enumerate(datafile):
            # concentrate returned np.ndarray
            x, y = _read_aimd_converge_data(df, index)
            xs.extend(x)
            ys.extend(y)
        xs = np.linspace(1, len(xs), len(xs))
        return xs, ys

    # search datafile in the given directory
    elif isinstance(datafile, str):
        if os.path.isdir(datafile):  # 如果是文件夹
            directory = datafile  # specified datafile is actually a directory
            print(f"您指定了一个文件夹，正在{directory}中自动查找aimd.h5...")
            if os.path.exists(os.path.join(directory, "aimd.h5")):
                datafile = os.path.join(directory, "aimd.h5")
                print("Reading aimd.h5...")
            else:
                raise FileNotFoundError("未找到aimd.h5文件！")

        elif datafile.endswith(".h5"):  # 如果是h5文件
            hf = h5py.File(datafile)  # 加载h5文件
            print(f" reading {os.path.abspath(datafile)}...")
            Nstep = len(np.array(hf.get("/Structures"))) - 2  # 步数（可能存在未完成的）
            ys = np.empty(Nstep)  # 准备一个空数组
            # 开始读取
            if index == "5":
                for i in range(1, Nstep + 1):
                    ys[i - 1] = np.linalg.det(hf.get("/Structures/Step-%d/Lattice" % i))
            else:
                map = {
                    "1": "IonsKineticEnergy",
                    "2": "TotalEnergy0",
                    "3": "PressureKinetic",
                    "4": "Temperature",
                }
                for i in range(1, Nstep + 1):
                    # 如果计算中断，则没有PressureKinetic这个键
                    try:
                        ys[i - 1] = np.array(
                            hf.get("/AimdInfo/Step-%d/%s" % (i, map[index]))
                        )
                    except:
                        ys[i - 1] = 0
                        ys = np.delete(ys, -1)
                        print(f"-> 计算中断于第 {Nstep} 步，未读取到第 {i} 步的 {map[index]} 数据！")
                        break

            Nstep = len(ys)  # 步数更新为实际完成的步数

            # 返回xs，ys两个数组
            return np.linspace(1, Nstep, Nstep), np.array(ys)

        else:
            raise TypeError("仅支持读取h5文件！")
    else:
        raise TypeError("datafile必须是字符串或列表！")
