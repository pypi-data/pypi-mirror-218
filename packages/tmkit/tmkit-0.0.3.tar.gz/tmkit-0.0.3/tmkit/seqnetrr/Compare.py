__author__ = "Jianfeng Sun"
__version__ = "v1.0"
__copyright__ = "Copyright 2023"
__license__ = "GPL v3.0"
__email__ = "jianfeng.sunmt@gmail.com"
__maintainer__ = "Jianfeng Sun"

import time
from tmkit.seqnetrr.window.Pair import Pair
from tmkit.seqnetrr.window.Single import Single
from tmkit.seqnetrr.combo.Length import length as plength
from tmkit.sequence import Fasta as sfasta
from tmkit.seqnetrr.combo.Position import Position as pfasta
from tmkit.seqnetrr.graph.Bipartite import Bipartite as bigraph
from tmkit.seqnetrr.graph.Unipartite import Unipartite as unigraph
from tmkit.seqnetrr.graph.Cumulative import Cumulative as cumugraph
from tmkit.util.Reader import Reader as prrcreader
from tmkit.util.Writer import Writer as pfwriter


class Compare:

    def __init__(
            self,
            fasta_path,
            window_size,
            seq_sep_inferior,
            pair_mode='patch',
            mode='hash',
            input_kind='general',
            list_fpn=None,
            fc_path=None,
            sv_fpn=None,
            is_sv=False,
            len_thres=500,
    ):
        """

        Parameters
        ----------
        fasta_path
        window_size
        seq_sep_inferior
        pair_mode
        mode
        input_kind
        list_fpn
        fc_path
        sv_fpn
        is_sv
        len_thres
        """
        self.sv_fpn = sv_fpn
        self.pfreader = prrcreader()
        self.pfwriter = pfwriter()
        self.is_sv = is_sv
        self.fc_path = fc_path
        self.seq_sep_inferior = seq_sep_inferior
        self.pair_mode = pair_mode
        self.mode = mode
        self.len_thres = len_thres
        self.input_kind = input_kind
        self.window_size = window_size
        self.prot_df = self.pfreader.generic(list_fpn)
        self.prot_df['len_seq'] = -1
        for i in self.prot_df.index:
            prot_name = self.prot_df.iloc[i, 0]
            file_chain = self.chain(self.prot_df.iloc[i, 1])
            sequence = sfasta.get(
                fasta_fpn=fasta_path + prot_name + file_chain + '.fasta',
            )
            # print(sequence)
            self.prot_df.loc[i, 'seq'] = sequence
            self.prot_df.loc[i, 'len_seq'] = len(sequence)
        self.prot_df = self.prot_df.loc[self.prot_df['len_seq'] < len_thres].reset_index(drop=True)
        print('Sequence separation inf: {}'.format(self.seq_sep_inferior))
        print('Length thres: {}'.format(self.len_thres))
        print('Window size: {}'.format(self.window_size))
        print('Input kind: {}'.format(self.input_kind))
        print('\n{}'.format(self.prot_df))
        print(self.prot_df.shape)

    def chain(self, prot_chain):
        """
        Chain name modification.

        Parameters
        ----------
        prot_chain
            chain of a protein in the prefix of a FASTA file name

        Returns
        -------
        str
            chain name

        """
        return str(prot_chain) + 'l' if str(prot_chain).islower() else str(prot_chain)

    def unipartite(self, mode):
        print('Mode: {}'.format(mode))
        for i in self.prot_df.index:
            stime = time.time()
            sequence = self.prot_df.loc[i, 'seq']
            prot_name = self.prot_df.iloc[i, 0]
            file_chain = self.chain(self.prot_df.iloc[i, 1])
            print('===>ID.{}'.format(i))
            print('===>protein: {}'.format(prot_name + file_chain))
            print('===>protein length: {}'.format(self.prot_df.loc[i, 'len_seq']))
            # /* scenario of position */
            pos_list = plength(seq_sep_inferior=self.seq_sep_inferior).to_pair(len(sequence))
            print('===>pair number: {}'.format(len(pos_list)))

            # /* position */
            position = pfasta(sequence).pair(pos_list=pos_list)

            # /* window */
            window_m_ids = Pair(
                sequence=sequence,
                position=position,
                window_size=self.window_size,
            ).mid()

            p = unigraph(
                sequence=sequence,
                window_size=self.window_size,
                window_m_ids=window_m_ids,
                input_kind=self.input_kind,
            )
            # /* local ec scores */
            list_2d = position
            p.assign(
                fpn=self.fc_path + prot_name + file_chain + '.evfold',
                list_2d=list_2d,
                mode=mode,
            )
            print('===>total time: {time}s.'.format(time=time.time() - stime))
            # print(vec)
            return 'Finished'

    def bipartite(self, pair_mode, mode):
        print('Pair mode: {}'.format(pair_mode))
        print('Mode: {}'.format(mode))
        for i in self.prot_df.index:
            stime = time.time()
            sequence = self.prot_df.loc[i, 'seq']
            prot_name = self.prot_df.iloc[i, 0]
            file_chain = self.chain(self.prot_df.iloc[i, 1])
            print('===>ID.{}'.format(i))
            print('===>protein: {}'.format(prot_name + file_chain))
            print('===>protein length: {}'.format(self.prot_df.loc[i, 'len_seq']))
            # /* scenario of position */
            pos_list = plength(seq_sep_inferior=self.seq_sep_inferior).to_pair(len(sequence))
            print('===>pair number: {}'.format(len(pos_list)))

            # /* position */
            position = pfasta(sequence).pair(pos_list=pos_list)

            # /* window */
            window_m_ids = Pair(
                sequence=sequence,
                position=position,
                window_size=self.window_size,
            ).mid()

            p = bigraph(
                sequence=sequence,
                window_size=self.window_size,
                window_m_ids=window_m_ids,
                kind=pair_mode,
                patch_size=2,
                input_kind=self.input_kind,
            )
            # /* global ec scores */
            list_2d = position
            p.assign(
                fpn=self.fc_path + prot_name + file_chain + '.evfold',
                list_2d=list_2d,
                mode=mode,
            )
            print('===>total time: {time}s.'.format(time=time.time() - stime))
            # print(vec)
            return 'Finished'

    def cumulative(self, cumu_ratio=0.5):
        print('cumulative ratio: {}'.format(cumu_ratio))
        for i in self.prot_df.index:
            stime = time.time()
            sequence = self.prot_df.loc[i, 'seq']
            prot_name = self.prot_df.iloc[i, 0]
            file_chain = self.chain(self.prot_df.iloc[i, 1])
            print('===>ID.{}'.format(i))
            print('===>protein: {}'.format(prot_name + file_chain))
            print('===>protein length: {}'.format(self.prot_df.loc[i, 'len_seq']))
            # /* scenario of position */
            pos_list = plength(seq_sep_inferior=self.seq_sep_inferior).tosgl(len(sequence))
            print('===>pair number: {}'.format(len(pos_list)))

            # /* position */
            position = pfasta(sequence).single(pos_list=pos_list)

            # /* window */
            window_m_ids = Single(
                sequence=sequence,
                position=position,
                window_size=self.window_size,
            ).mid()

            p = cumugraph(
                sequence=sequence,
                window_size=self.window_size,
                window_m_ids=window_m_ids,
                input_kind=self.input_kind,
            )
            # /* global ec scores */
            list_2d = position
            p.assign(
                list_2d=list_2d,
                fpn=self.fc_path + prot_name + file_chain + '.evfold',
                L=int(len(sequence) * cumu_ratio),
                simu_seq_len=None,
            )
            print('===>total time: {time}s.'.format(time=time.time() - stime))
            return 'Finished'
