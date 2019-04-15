# This program adds region features
# like cortical thickness or surface area etc to the existing parcellation table
import os
import json
import warnings

BASE_DIR = "/home/turja"
STAT_DIR = BASE_DIR + "/AD_stats"  # FreeSurfer statistics
PARC_DIR = BASE_DIR + "/AD_parc"  # Parcellation tables


def get_stat_file(subject):
    lhem_stat = os.path.join(STAT_DIR + "/" + subject, "lh.aparc.a2009s.stats")
    rhem_stat = os.path.join(STAT_DIR + "/" + subject, "rh.aparc.a2009s.stats")
    return lhem_stat, rhem_stat


def get_feat_dict(file):
    hem_feat = []
    with open(file, 'r+') as lf:
        line = lf.readline()
        col_head_dict = {}
        while not line.startswith("# TableCol"):
            line = lf.readline()

        # Parse column head information
        while line.startswith("# "):
            if "ColHeader" not in line:
                line = lf.readline()
                continue

            fields = line.split()
            if len(fields) > 5:
                break
            col_head_dict[int(fields[2]) - 1] = fields[4]
            line = lf.readline()

        for line in lf:
            feat_dict = {}
            field_val = line.split()
            for i, feat in enumerate(field_val):
                feat_dict[col_head_dict[i]] = feat
            hem_feat.append(feat_dict)
    return hem_feat


def generate_parc_table(subject):
    # Read features for right and left hemisphere
    lfile, rfile = get_stat_file(subject)
    lhem_feat = get_feat_dict(lfile)
    rhem_feat = get_feat_dict(rfile)
    parc_file = os.path.join(PARC_DIR, subject + '_parcellationTable.json')

    # Read parcellation table
    try:
        with open(parc_file, 'r+') as parc:
            parc_table = json.load(parc)
            if len(parc_table) == 152:
                del parc_table[118]
                del parc_table[76]
                del parc_table[42]
                del parc_table[0]
            elif len(parc_table) != 148:
                warnings.warn(subject + " >> parcellation table size should be 148. Got: " + len(parc_table))
    except FileNotFoundError:
        warnings.warn("Corresponding network data does not exist. Skipping.")
        return

    for i, r in enumerate(parc_table):
        if i < len(parc_table) / 2:
            # Checking if we are at the right entry. This will raise warning if
            # the order of stat and previous parc table do not match
            if r["name"] != lhem_feat[i]["StructName"] or r["VisuHierarchy"] != "seed.left":
                warnings.warn(subject + " >> Region mismatch: \tExpected " \
                                                      + lhem_feat[i]["StructName"] + "\tGot: " + r["name"])
                return
            else:
                for k, v in lhem_feat[i].items():
                    if not k == "StructName":  # Ignoring this as it's already in "name"
                        r[k] = v
        else:
            if r["name"] != rhem_feat[i - len(parc_table) // 2]["StructName"] or r["VisuHierarchy"] != "seed.right":
                warnings.warn(subject + " >> Region mismatch: \tExpected " \
                                                      + rhem_feat[i - len(parc_table) // 2]["StructName"] + "\tGot: " + r["name"])
                return
            else:
                for k, v in rhem_feat[i - len(parc_table) // 2].items():
                    if not k == "StructName":
                        r[k] = v

    # Write file
    with open(parc_file, 'w+') as f:
        json.dump(parc_table, f)
    return parc_table


if __name__ == '__main__':
    for subject in os.listdir(STAT_DIR):
        generate_parc_table(subject)
