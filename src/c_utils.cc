#ifndef DIJET_UTILS_C
#define DIJET_UTILS_C

auto id_pair(ROOT::RVec<float> v, ROOT::RVec<int> idx) {
ROOT::RVec<float> result;
int size = Max(idx)+1;
result.resize(size);

for (int i=0; i<idx.size(); i++) {
    if (idx[i] >= 0) {
        result[idx[i]] = v[i];
    }
}

return result;
}

auto id_filter(ROOT::RVec<float> v, ROOT::RVec<int> idx) {
ROOT::RVec<float> result;
int size = Max(idx)+1, idx_size = idx.size();
result.resize(size);

for (int i=0; i<idx_size; i++){
    if (idx[i] >= 0) {
        result[idx[i]] = v[idx[i]];
    }
}

return result;
}
