import { Component, OnInit } from '@angular/core';
import { FileService } from 'src/app/Services/file/file.service';
import { MatSnackBar } from '@angular/material/snack-bar';

import File from 'src/app/Models/file.model';

@Component({
  selector: 'app-file-view',
  templateUrl: './file-view.component.html',
  styleUrls: ['./file-view.component.css']
})
export class FileViewComponent implements OnInit {
  file : File = {};
  path : string[] = []; 

  constructor(
    private snackBar: MatSnackBar,
    private fileService:FileService) { }

  ngOnInit(): void {
  }

  public getCurrentPath() {
    var tmp_path = '';
    this.path.forEach((segment) => {
      tmp_path = tmp_path.concat(segment + '/');
    });
    return tmp_path;
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
      this.snackBar.open("Archivo actualizado", 'Cerrar', {
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
