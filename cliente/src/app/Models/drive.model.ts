import Directory from "./directory.model";
import File from "./file.model";


interface Drive {
    name?: string;
    directories?: Directory[];
    files?: File[];

}
  
export default Drive;