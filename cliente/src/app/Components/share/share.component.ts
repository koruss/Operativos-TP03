import { Component, OnInit } from '@angular/core';
import { DriveService } from 'src/app/Services/drive/drive.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { FileService } from 'src/app/Services/file/file.service';
import { DirectoryService } from 'src/app/Services/directory/directory.service';

@Component({
  selector: 'app-share',
  templateUrl: './share.component.html',
  styleUrls: ['./share.component.css']
})
export class ShareComponent implements OnInit {
  users:string[] = [];
  filePath: string = "";
  fileName: string = "";
  destinyUsername: string = "";
  type: boolean = true;

  constructor(private driveService : DriveService,
              private snackBar : MatSnackBar,
              private fileService: FileService,
              private dirService: DirectoryService ) { }

  public async ngOnInit(): Promise<void> {
    if(this.users.length==0)
      await this.getUsers();
  }

  /**
   * get users
   * @returns void
   */
   public async getUsers():Promise<void> {
    try {
      
      let response = await this.driveService.getUsers();
      this.users = response.users
      
    } catch (err: any) {
      const { message } = err.error;
      this.snackBar.open(message, 'Close', {
        verticalPosition: 'top',
        duration: 3000,
      });
    }
  }

  /**
   * Shares a selected file
   */
  public async onClickShareFile(user: any){
    
    try {
      if(this.type){
        let file = {fileName: this.fileName,filePath: this.filePath,destinyUsername:user,forceOverwrite:true}
        console.log(file);
        await this.fileService.shareFile(file);
        
        this.snackBar.open("File shared successfully", 'Close', {
          verticalPosition: 'top',
          duration: 3000,
        });
      }
        

      else{
        let dir = {dirName: this.fileName,dirPath: this.filePath,destinyUsername:user,forceOverwrite:true}
        console.log(1111111111);
        await this.dirService.shareDir(dir);

        this.snackBar.open("Folder shared successfully", 'Close', {
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
