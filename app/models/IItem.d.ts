export interface IItem {
  id: string;
  name: string;
  shortName: string;
  normalizedName: string;
  description: null | string;
  basePrice: number;
  weight: number;
  height: number;
  image8xLink: string;
  inspectImageLink: string;
  gridImageLink: string;
  avg24hPrice: null | number;
  link: string;
  wikiLink: string;
  minLevelForFlea: number,
  sellFor: {
    price: number;
    currency: string;
    priceRUB: number;
    vendor: {
      name: string;
      normalizedName: string;
    };
  }[];
}
