import numpy as np
import matplotlib.pyplot as plt
import argparse, time, matplotlib
import quantum_matched_filter_functions as qmffn
import matplotlib.animation as animation

np.random.seed(int(time.time()))

def main(infile, outpath, bank='bank', fontsize=28, ticksize=22, figsize=(14,11), tempfile=None):

    if bank=='bank':
        bankfunc = qmffn.get_paras
    elif bank=='grid':
        bankfunc = qmffn.get_mass_grid
        spins=False
    else:
        raise ValueError(bank+' is not an option. Try either "bank" or "grid".')
        exit()

    matplotlib.rcParams['mathtext.fontset'] = 'stix'
    matplotlib.rcParams['font.family'] = 'STIXGeneral'

    psi_1 = np.load(infile)

    match_ind = np.argmax(np.sum(np.abs(psi_1)**2,axis=1))
    nmatch_ind = np.argmin(np.sum(np.abs(psi_1)**2,axis=1))

    psi_match = psi_1[match_ind]
    psi_nmatch = psi_1[nmatch_ind]

    label_match = r'$\rho \geq \rho_{\mathregular{th}}$'
    label_nmatch = r'$\rho < \rho_{\mathregular{th}}$'
    ylabel = r'Probability amplitude'
    xlabel = r'$i$'

    M = psi_1.shape[0]

    temp_bank, M1, M2 = bankfunc(M, temp_file=tempfile)

    fig, axs = plt.subplots(2,1, figsize=figsize)

    axs[0].set_xlabel(r'$m_{1}$', fontsize=fontsize)
    axs[0].set_ylabel(r'$m_{2}$', fontsize=fontsize)
    #axs[0].set_xlim(0.,150)

    axs[0].tick_params(axis='both', labelsize=ticksize)
    axs[1].tick_params(axis='both', labelsize=ticksize)

    axs[1].plot(psi_1[match_ind], color='black', lw=2, label=label_match)
    axs[1].plot(psi_1[nmatch_ind], ls='--', color='black', lw=2, label=label_nmatch)
    axs[1].set_xlabel(r'$i$', fontsize=fontsize)
    axs[1].set_ylabel(r'Probability amplitude', fontsize=fontsize)

    plt.tight_layout()

    ims = []
    for p in np.arange(psi_1.shape[1]):
        sc = axs[0].scatter(temp_bank['mass1'], temp_bank['mass2'], c=psi_1[:,p], marker='.', lw=3*(np.abs(psi_1[:,p])**2)/np.max(np.abs(psi_1)**2), alpha=0.5, vmin=np.min(psi_1), vmax=np.max(psi_1), label=r'$p=$'+str(p), cmap=matplotlib.cm.twilight_shifted)
        ims.append((sc,axs[1].vlines(p,ymin=np.min(psi_1),ymax=np.max(psi_1), color='black'),))

    cblabel='Probability amplitude'
    cb = plt.colorbar(sc, label=cblabel, ax=[axs])#[axs[0]])
    #cb.ax.tick_params(labelsize=ticksize) 
    #cb.ax.get_yticklabels(fontsize=fontsize)
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=5, metadata=dict(artist='Me'), bitrate=1800)
    im_ani = animation.ArtistAnimation(fig, ims, interval=50, repeat_delay=3000, blit=True)
    im_ani.save(outpath+'.'.join(infile.split('/')[-1].split('.')[:-1])+'_mass_ani.mp4', writer=writer)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='', description="Perform one QMF on GW150914 given a template bank")
    parser.add_argument('--infile', help="", type=str, required=True)
    parser.add_argument('--outpath', help="", type=str, required=True)
    parser.add_argument('--bank', help="", type=str, default='bank')
    parser.add_argument('--tempfile', help="", type=str, default=None)

    opt = parser.parse_args()
 
    main(opt.infile, opt.outpath, bank=opt.bank, tempfile=opt.tempfile)
