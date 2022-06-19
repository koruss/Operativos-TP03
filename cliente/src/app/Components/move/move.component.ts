import { Component, OnInit } from '@angular/core';
import { DirectoryService } from '../../Services/directory/directory.service';
import { FileService } from '../../Services/file/file.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { DriveService } from '../../Services/drive/drive.service';


import Directory from '../../Models/directory.model';
import User from '../../Models/user.model';
import Drive from '../../Models/drive.model';




@Component({
  selector: 'app-move',
  templateUrl: './move.component.html',
  styleUrls: ['./move.component.css']
})
export class MoveComponent implements OnInit {
  path: string[] = [];
  directories: Directory[] = [];
  user: User = {};
  directory: Drive = {};
  file: string = "{}";
  filePath: string = "{}";
  move:boolean = true;
  type: boolean = true;

  drives = [1,2,3,4]
  constructor(
    private dirService: DirectoryService,
    private fileService: FileService,
    private snackBar: MatSnackBar,
    private driveService: DriveService,) { }

  async ngOnInit(): Promise<void> {
    if (this.user.username != null) {
      await this.getDir(this.user.username + '/root');
      this.path.push('root');
    }
  }

  /**
   * Get Current path
   * @returns current path
   */
   public getCurrentPath() {
    let path = this.user.username + '/';
    this.path.forEach((segment) => {
      path = path.concat(segment + '/');
    });
    return path;
  }

  /**
   * Change Dir to selected Dir
   * @returns void
   */
   public async onClickChangeDirForward(path: any) {
    this.path.push(path);
    this.driveService.appendDirectoryToPath(path);
    await this.getDir(this.getCurrentPath() + path);
  }

  /**
   * Change Dir to selected Dir
   * @returns void
   */
  public async onClickChangeDirBackward() {
    if(this.path.length > 1)
      this.path.pop();
    if(this.path.length != 0)
      await this.getDir(this.getCurrentPath());
  }

    /**
   * Get dir from specific path
   * @returns void
   */
     public async getDir(path: string): Promise<void> {
      try {
        this.directory = await this.dirService.getDir(path);
        this.directories = this.directory.directories as Directory[];
      } catch (err: any) {
        const { message } = err.error;
        this.snackBar.open(message, 'Close', {
          verticalPosition: 'top',
          duration: 3000,
        });
      }
    }

    /**
   * Moves a selected file
   */
    public async OnClickMove(): Promise<void>{
      
      try {
        if(this.type){
          let file = {fileName: this.file,filePath: this.filePath,destinyPath:this.getCurrentPath(),forceOverwrite:true}
          
          await this.fileService.moveFile(file);
          this.snackBar.open("File moved successfully", 'Close', {
          verticalPosition: 'top',
          duration: 3000,
          });
        }

        else{
          let dir = {dirName: this.file,dirPath: this.filePath,destinyPath:this.getCurrentPath(),forceOverwrite:true}
          
          await this.dirService.moveDir(dir);
          this.snackBar.open("Directory moved successfully", 'Close', {
          verticalPosition: 'top',
          duration: 3000,
          });
        }
        
        
      } catch (err: any) {
        console.log(err.error);
        const { message } = err.error;
        this.snackBar.open(message, 'Close', {
          verticalPosition: 'top',
          duration: 3000,
        });
      }
    }
    
    /**
   * Copies a selected file
   */
    public async OnClickCopy(): Promise<void>{
      
      try {

        if(this.type){
          
          let file = {fileName: this.file,filePath: this.filePath,destinyPath:this.getCurrentPath(),forceOverwrite:true}
          console.log(file);
          await this.fileService.copyFile(file);
          this.snackBar.open("File copied successfully", 'Close', {
          verticalPosition: 'top',
          duration: 3000,
          });
        }

        else{
          let dir = {dirName: this.file,dirPath: this.filePath,destinyPath:this.getCurrentPath(),forceOverwrite:true}
          console.log(dir);
          await this.dirService.copyDir(dir);
          this.snackBar.open("Directory copied successfully", 'Close', {
          verticalPosition: 'top',
          duration: 3000,
          });
        }
        
        
      } catch (err: any) {
        console.log(err.error);
        const { message } = err.error;
        this.snackBar.open(message, 'Close', {
          verticalPosition: 'top',
          duration: 3000,
        });
      }
    }

}
