export interface ITrader {
  name: string;
  normalizedName: string;
  imageLink: string;
  image4xLink: string;
  currency: {
    name: string;
    normalizedName: string;
    shortName: string;
  };
}
