
"""5' defects"""
import csv  #RD
import logging
import os.path

from Bio import SeqIO  #RD

from .utils import find_gapped_pos  #RD

logger = logging.getLogger('pipe.defect')

def _detect_defect(ref, qry, pos_start, pos_end):
    # Find tag position in reference seq, and start aln pos for the rest. #RD
    pos_start = find_gapped_pos(ref, pos=pos_start - 1)[0]  #RD
    pos_end = find_gapped_pos(ref, pos=pos_end - 1)[0]  #RD

    n_del = 0
    n_ins = 0
    for char_ref, char_qry in zip(ref.seq[pos_start:pos_end],
                                  qry.seq[pos_start:pos_end]):
        if (char_ref != '-') and (char_qry == '-'):
            n_del += 1
        elif (char_ref == '-') and (char_qry != '-'):
            n_ins += 1
    return n_del, n_ins

def defect(configs, seqs):
    """Determine if a contig has 5' defect in the tag region."""
    # Logging
    logger.info("Checking 5' defects")
    file_aln = configs['file_aln']
    try:
        f_size = os.path.getsize(file_aln)
    except OSError:
        f_size = 0

    if f_size > 0:
        max_gaps = int(configs['max_gaps'])
        pos_start = int(configs['start'])
        pos_end = int(configs['end'])

        aln = SeqIO.parse(file_aln, 'fasta')
        ref = next(aln)
        for qry in aln:
            qid = qry.id
            # qid = qid.rstrip('_Genome')  #RD original behavior (unsafe) #RD
            if qid.endswith('_Genome'):  #RD
                qid = qid[:-7]  #RD
            n_del, n_ins = _detect_defect(ref, qry, pos_start, pos_end)

            if n_del >= max_gaps:
                if seqs.call[qid]['primer'] == 'No':
                    seqs.call[qid]['defect'] = 'Possible'
                    seqs.comments[qid] += "Missing primer for 5' defect;"
                else:
                    seqs.call[qid]['defect'] = 'Yes'
            else:
                seqs.call[qid]['defect'] = 'No'

            seqs.info[qid]['defect'] = (n_del, n_ins)
    for qid in seqs.qids:
        if 'defect' not in seqs.call[qid]:
            seqs.call[qid]['defect'] = 'Pass'
            seqs.info[qid]['defect'] = ['Pass', 'Pass']

    csv_path = "5prime_deletions_summary.csv"
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['sequence_id', 'deletion_type', 'start_pos', 'end_pos', 'deletion_length']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for qid in seqs.qids:
            defect_status = seqs.call[qid].get('defect', 'Unknown')
            n_del, _ = seqs.info[qid].get('defect', (0, 0))
            deletion_type = '5prime_deletion' if defect_status in ('Yes', 'Possible') else 'None'

            writer.writerow({
                'sequence_id': qid,
                'deletion_type': deletion_type,
                'start_pos': configs['start'],
                'end_pos': configs['end'],
                'deletion_length': n_del
            })
    logger.info("Wrote 5prime_deletions_summary.csv")  #RD
    with open(configs['file_out'], 'w') as fh_o:
        print("Contig ID\tGaps\tInserts\t5' Defect", file=fh_o)
        for qid in seqs.qids:
            print('{}\t{}\t{}\t{}'.format(qid, *seqs.info[qid]['defect'], seqs.call[qid]['defect']), file=fh_o)
