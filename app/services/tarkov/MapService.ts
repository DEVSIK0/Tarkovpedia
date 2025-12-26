import type { IMap } from "~/models/IMap";

export class MapService {
  static MAPS: IMap[] = [
    {
      name: "Customs",
      shortName: "customs",
      fileName: "customs.webp",
      fileThumbnail: "customs_thumbnail.webp",
      aspectRatio: [0, 0],
    },
    {
      name: "Factory",
      shortName: "factory",
      fileName: "factory.webp",
      fileThumbnail: "factory_thumbnail.webp",
      aspectRatio: [0, 0],
    },
    {
      name: "Ground Zero",
      shortName: "zero",
      fileName: "ground_zero.webp",
      fileThumbnail: "ground_zero_thumbnail.webp",
      aspectRatio: [0, 0],
    },
    {
      name: "Interchange",
      shortName: "interchange",
      fileName: "interchange.webp",
      fileThumbnail: "interchange_thumbnail.webp",
      aspectRatio: [0, 0],
    },
    {
      name: "Labyrinth",
      shortName: "labyrinth",
      fileName: "labyrinth.webp",
      fileThumbnail: "labyrinth_thumbnail.webp",
      aspectRatio: [0, 0],
    },
    {
      name: "Lighthouse",
      shortName: "lighthouse",
      fileName: "lighthouse.webp",
      fileThumbnail: "lighthouse_thumbnail.webp",
      aspectRatio: [0, 0],
    },
    {
      name: "Reserve",
      shortName: "reserve",
      fileName: "reserve.webp",
      fileThumbnail: "reserve_thumbnail.webp",
      aspectRatio: [0, 0],
    },
    {
      name: "Shoreline",
      shortName: "shoreline",
      fileName: "shoreline.webp",
      fileThumbnail: "shoreline_thumbnail.webp",
      aspectRatio: [0, 0],
    },
    {
      name: "Streets of Tarkov",
      shortName: "streets",
      fileName: "streets_of_tarkov.webp",
      fileThumbnail: "streets_of_tarkov_thumbnail.webp",
      aspectRatio: [0, 0],
    },
    {
      name: "Woods",
      shortName: "woods",
      fileName: "woods.webp",
      fileThumbnail: "woods_thumbnail.webp",
      aspectRatio: [0, 0],
    },
    {
      name: "Labs",
      shortName: "labs",
      fileName: "labs.webp",
      fileThumbnail: "labs_thumbnail.webp",
      aspectRatio: [0, 0],
    },
  ];

  public static async getAllMaps(): Promise<IMap[]> {
    return this.MAPS;
  }
}
