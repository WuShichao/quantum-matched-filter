import numpy as np
import gw_detections_functions as gwfn
import quantum_matched_filter_functions as qmffn
import argparse, time

np.random.seed(int(time.time()))

def main(Mqubits, Pqubits, tag='out', path='./output/', SNR_threshold=12., bank='bank', data_file='data/signal.npy', psd_file='data/psd.npy', template_file='data/template_bank.hdf', spins=True, cores=1):
    
    if bank=='bank':
        bankfunc = qmffn.get_paras
    elif bank=='grid':
        bankfunc = qmffn.get_mass_grid
        spins=False
    else:
        raise ValueError(bank+' is not an option. Try either "bank" or "grid".')
        exit()

    Data = np.load(data_file)
    psd = np.load(psd_file)
    
    M = 2**Mqubits
    P = 2**Pqubits

    tag = str(M)+'_'+str(P)+'_'+str(SNR_threshold).replace('.','_')+'_'+tag

    measurement, psi_opt, Nmatches = qmffn.QMF(Data, psd, M, P, tag=tag, path=path, SNR_threshold=SNR_threshold, bankfunc=bankfunc, table=False, save_states=True, dtype='float64', temp_file=template_file, spins=spins, cores=cores)

    print(measurement)
    N_templates = int(np.round(M*np.sin(measurement*np.pi/P)**2))
    opt_p = int(np.round(((np.pi/4)/np.arcsin(np.sqrt(N_templates/M))) - 1./2))
    print(opt_p)
    print(N_templates, Nmatches)
    print(np.sum(np.abs(psi_opt[np.abs(psi_opt)**2>np.mean(np.abs(psi_opt)**2)])**2))

    np.save(path+'psi_opt_'+tag,psi_opt)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='', description="Perform one QMF on GW150914 given a template bank")
    parser.add_argument('--tag', help="Name tag", type=str, required=True)
    parser.add_argument('--Mq', help="Template qubits", type=int, default=8)
    parser.add_argument('--Pq', help="Precision qubits", type=int, default=7)
    parser.add_argument('--SNR-thr', help="SNR threshold", type=float, default=12.)
    parser.add_argument('--data-file', help="", type=str, default='data/signal.npy')
    parser.add_argument('--psd-file', help="", type=str, default='data/psd.npy')
    parser.add_argument('--temp-file', help="", type=str, default='data/template_bank.hdf')
    parser.add_argument('--path', help="", type=str, default='./output/')
    parser.add_argument('--bank', help='Either "bank" or "grid"', type=str, default='bank')
    parser.add_argument('--spinless', help='Turn off spins', action='store_false')
    parser.add_argument('--cores', help="Number of cores", type=int, default=1)

    opt = parser.parse_args()
 
    main(opt.Mq, opt.Pq, tag=opt.tag, path=opt.path, SNR_threshold=opt.SNR_thr, bank=opt.bank, data_file=opt.data_file, psd_file=opt.psd_file, template_file=opt.temp_file, spins=opt.spinless, cores=opt.cores)
