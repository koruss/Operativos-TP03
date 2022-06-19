interface File {
    name?: string;
    extension?: string;
    creation?: string;  //(YYYY-MM-DD HH:MM:SS),
    modification?: string; //(YYYY-MM-DD HH:MM:SS),
    size?: number;
    content?: string;

}
  
export default File;

