import numpy as np
# from scipy import interpolate  
from .logging import logger

@logger.catch
def align_joint_eeg_em_data(eeg_d, eeg_t, em_d, em_t):
    '''
    Joint the EEG(eeg) and EyeMovement(em) data.
    And time align them with eeg_t.
    '''
    eeg_d = np.array(eeg_d)
    
    if em_d is None:
        resampled_value = np.zeros((len(eeg_d), 4))
    else:
        original_t = np.array(em_t)
        original_value = np.array(em_d)
        t1 = eeg_t[0]
        t2 = eeg_t[-1] + 0.04
        target_t = np.linspace(t1, t2, len(eeg_d))
        buf = []
        for d in original_value.transpose():
            buf.append(np.interp(target_t, original_t, d))
        resampled_value = np.array(buf).transpose()
    
    em_d = np.array(resampled_value)
    return np.concatenate([eeg_d, em_d], axis=1)