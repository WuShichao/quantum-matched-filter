import numpy as np
import matplotlib.pyplot as plt
import argparse, time, matplotlib

np.random.seed(int(time.time()))

def main(infile, outpath, noisefile=None, snrfile=None, fontsize=28, ticksize=22, figsize=(18,5)):

    matplotlib.rcParams['mathtext.fontset'] = 'stix'
    matplotlib.rcParams['font.family'] = 'STIXGeneral'

    psi_2 = np.load(infile)

    fig = plt.figure(figsize=figsize)
    ax = fig.gca()

    M = psi_2.shape[1]
    P = psi_2.shape[0]
    bs = np.arange(psi_2.shape[0])
    probs = np.sum(np.absolute(psi_2).T**2,axis=0)
    
    theta_t = np.where(bs<P/2,bs*np.pi/P,(bs*np.pi/P)+np.pi)
    matches = np.floor(M*np.sin(theta_t)**2)

    match_probs = np.zeros(len(np.unique(matches)))

    for i,match in enumerate(np.unique(matches)):
        match_probs[i] = np.sum(probs[match==matches])

    ax.set_xlabel(r'$b$', fontsize=fontsize)
    ax.set_ylabel(r'$p(b)$', fontsize=fontsize)
    ax.tick_params(axis='both', labelsize=ticksize)
    lw=5
    ms=10
    ax.plot(np.unique(matches), match_probs, color='black', marker='o', lw=0., ms=ms, label='Result given GW150914')
    delta = 0.0
    for match, match_prob in zip(np.unique(matches), match_probs):
        ax.axvline(match, ymin=0.+delta, ymax=match_prob+delta, color='black', ls='-', lw=lw)

    if noisefile:
        psi_2 = np.load(noisefile)
        M = psi_2.shape[1]
        P = psi_2.shape[0]
        bs = np.arange(psi_2.shape[0])
        probs = np.sum(np.absolute(psi_2).T**2,axis=0)

        theta_t = np.where(bs<P/2,bs*np.pi/P,(bs*np.pi/P)+np.pi)
        matches = np.floor(M*np.sin(theta_t)**2)

        match_probs = np.zeros(len(np.unique(matches)))

        for i,match in enumerate(np.unique(matches)):
            match_probs[i] = np.sum(probs[match==matches])

        ax.plot(np.unique(matches), match_probs, color='red', marker='o', lw=0., ms=ms, label='Result given detector data without a signal')
        for match, match_prob in zip(np.unique(matches), match_probs):
            ax.axvline(match, ymin=0.+delta, ymax=match_prob+delta, color='red', ls='-', lw=lw)

    if snrfile:
        snrs = np.load(snrfile)
        snr_th = float(infile.split('/')[-1].split('_')[4])
        matches_T = np.sum(snrs>=snr_th)
        ax.axvline(matches_T, ymin=0.,ymax=1., color='black', ls=':', label='True number of matches', lw=lw)


    leg = ax.legend(loc='upper left', fontsize=fontsize)
    leg.get_frame().set_linewidth(0.0)
    ax.set_xlabel(r'Number of matching templates from counting', fontsize=fontsize)
    ax.set_ylabel(r'Probability', fontsize=fontsize)
    ax.tick_params(axis='both', labelsize=ticksize)
    ax.set_xscale('symlog')
    ax.set_xlim(-0.1)
    ax.set_ylim(0.,1.)
    fig.savefig(outpath+'.'.join(infile.split('/')[-1].split('.')[:-1])+'_psi2_matches.png',bbox_inches='tight')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='', description="Perform one QMF on GW150914 given a template bank")
    parser.add_argument('--infile', help="", type=str, nargs='+', required=True)
    parser.add_argument('--outpath', help="", type=str, required=True)
    parser.add_argument('--noisefile', help="", type=str, default=False)
    parser.add_argument('--snrfile', help="", type=str, default=False)

    opt = parser.parse_args()
 
    main(opt.infile, opt.outpath, noisefile=opt.noisefile, snrfile=opt.snrfile)
