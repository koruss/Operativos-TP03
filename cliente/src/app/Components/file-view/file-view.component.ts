import { Component, OnInit } from '@angular/core';
import { FileService } from 'src/app/Services/file/file.service';
import { MatSnackBar } from '@angular/material/snack-bar';

import File from 'src/app/Models/file.model';
import User from 'src/app/Models/user.model';

@Component({
  selector: 'app-file-view',
  templateUrl: './file-view.component.html',
  styleUrls: ['./file-view.component.css']
})
export class FileViewComponent implements OnInit {
  file : File = {};
  path : string[] = []; 
  user : User = {};

  constructor(
    private snackBar: MatSnackBar,
    private fileService:FileService) { }

  ngOnInit(): void {
  }

  /**
   * Get Current path
   * @returns current path
   */
   public getCurrentPath(){
    let path = this.user.username + '/';
    this.path.forEach(segment => {
      path = path.concat(segment+'/');
    });
    return path;
  }

  /**
   * Update file
   * @returns void
   */
  public async  updateFile(){
    try {
    let modifiedFile = {"filePath": this.getCurrentPath(),
                        "fileName": this.file.name,
                        "content": this.file.content
                       };
                       console.log(modifiedFile);
      await this.fileService.modifyFile(modifiedFile);
      this.snackBar.open("File updated correctly", 'Close', {
        verticalPosition: 'top',
        duration: 3000,
      });

    } catch (err: any) {
      const { message } = err.error;
      this.snackBar.open(message, 'Close', {
        verticalPosition: 'top',
        duration: 3000,
      });
    }
    
  }

}
