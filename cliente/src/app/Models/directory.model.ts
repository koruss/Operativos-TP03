import File from "./file.model";

interface Directory {
    name?: string;
    directories?: Directory[];
    files?: File[];

}
  
export default Directory;