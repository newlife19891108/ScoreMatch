from dtwMatch import *
from rank import *
from chromagram import *

template = "./csv_samples/TeVasMilongaOrig_vamp_nnls-chroma_nnls-chroma_bothchroma.csv"
candidates = ["./csv_samples/TeVasMilongabeg_vamp_nnls-chroma_nnls-chroma_bothchroma.csv",
"./csv_samples/tevasmilongareal_vamp_nnls-chroma_nnls-chroma_bothchroma.csv",
"./csv_samples/sakura_vamp_nnls-chroma_nnls-chroma_bothchroma.csv",
"./csv_samples/sakuracut_vamp_nnls-chroma_nnls-chroma_bothchroma.csv",
"./csv_samples/tevasmilongarealcut_vamp_nnls-chroma_nnls-chroma_bothchroma.csv"
,"./csv_samples/tevascut_vamp_nnls-chroma_nnls-chroma_bothchroma.csv"]
print rank(template,candidates,getChromagramFromCSV,rdtwGlobalMatchScore)
print rank(template,candidates,getChromagramFromCSV,rdtwSubsequenceMatchScore)
template ="./csv_samples/TeVasMilongaOrigMidi.csv"
candidates=["./csv_samples/TeVasMilongabeg_vamp_vamp-hpcp-mtg_MTG-HPCP_HPCP.csv",
"./csv_samples/tevasmilongareal_vamp_vamp-hpcp-mtg_MTG-HPCP_HPCP.csv",
"./csv_samples/sakura_vamp_vamp-hpcp-mtg_MTG-HPCP_HPCP.csv",
"./csv_samples/sakuracut_vamp_vamp-hpcp-mtg_MTG-HPCP_HPCP.csv",
"./csv_samples/tevasmilongarealcut_vamp_vamp-hpcp-mtg_MTG-HPCP_HPCP.csv",
"./csv_samples/tevascut_vamp_vamp-hpcp-mtg_MTG-HPCP_HPCP.csv"
,"./csv_samples/puebloblanco_vamp_vamp-hpcp-mtg_MTG-HPCP_HPCP.csv"]
print rank(template,candidates,getChromagramFromCSV,rdtwSubsequenceMatchScore)
print rank(template,candidates,getChromagramFromCSV,rdtwGlobalMatchScore)
