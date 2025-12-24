import { TraderService } from "@/services/tarkov/TraderService";
import type { ITrader } from "@/models/ITrader";

export const useTraders = defineStore("traders", () => {
  const traders = ref<ITrader[] | null>(null);
  const fetchTraders = () => {
    TraderService.getAllTraders().then((response) => {
      traders.value = response.map((trader) => {
        if (trader.normalizedName === "btr-driver") {
          trader.normalizedName = "flea-market";
          trader.image4xLink = "/images/flea.svg";
        }
        return trader;
      });
    });
  };

  return {
    traders,
    fetchTraders,
  };
});
