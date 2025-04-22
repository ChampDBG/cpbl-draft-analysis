import pandas as pd


class AdvStat:
    def __init__(self, bat_data_path: str):
        self._bat_data = pd.read_csv(bat_data_path)
        self._bat_data["OBP"] = self._calc_obp(data=self._bat_data)
        self._bat_data["SLG"] = self._calc_slg(data=self._bat_data)
        self._bat_data["OPS"] = self._calc_ops(data=self._bat_data)
        self._calc_ops_plus(data=self._bat_data)

    def _calc_obp(self, data):
        """
        (H + BB + HBP) / (AB + BB + SF + HBP)
        """

        numerator = data["H"] + data["BB"] + data["HBP"]
        denominator = data["AB"] + data["BB"] + data["HBP"] + data["SF"]
        return numerator / denominator

    def _calc_slg(self, data):
        """
        TB / AB
        """
        return data["TB"] / data["AB"]

    def _calc_ops(self, data):
        """
        OPS = SLG + OBP
        """
        return data["OBP"] + data["SLG"]

    def _calc_ops_plus(self, data):
        self._lg_obs = dict()
        self._lg_slg = dict()

        years = [2020, 2021, 2022, 2023, 2024]
        grade = ["一軍", "二軍"]
        self._bat_data["OPSplus"] = 0.0

        for y in years:
            for g in grade:
                index = (data["年度"] == y) & (data["階級"] == g)
                d_tmp = data[index]

                agg_data = d_tmp[["AB", "H", "BB", "HBP", "SF", "TB"]].sum()
                lg_obs = self._calc_obp(agg_data)
                lg_slg = self._calc_slg(agg_data)

                self._bat_data.loc[index, "OPSplus"] = (
                    (self._bat_data.loc[index, "OBP"] / lg_obs)
                    + (self._bat_data.loc[index, "SLG"] / lg_slg)
                    - 1
                )
                self._lg_obs[f"{y}_{g}"] = lg_obs
                self._lg_slg[f"{y}_{g}"] = lg_slg


def main():
    adv_stat = AdvStat("data/batting/stat.csv")
    adv_stat._bat_data.to_csv("data/batting/adv_stat.csv")


if __name__ == "__main__":
    main()
