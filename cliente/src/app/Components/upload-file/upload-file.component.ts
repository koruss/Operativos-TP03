import { Component, OnInit } from '@angular/core';
import { FileService } from '../../Services/file/file.service';
import { DriveService } from '../../Services/drive/drive.service';
import { AuthenticationService } from '../../Services/authentication/authentication.service';

import { MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-upload-file',
  templateUrl: './upload-file.component.html',
  styleUrls: ['./upload-file.component.css'],
})
export class UploadFileComponent implements OnInit {
  public isNameRepeated: boolean = false;
  public selectedFile: File | undefined;

  constructor(
    private fileService: FileService,
    private driveService: DriveService,
    private authService: AuthenticationService,
    private snackBar: MatSnackBar,
    public dialogRef: MatDialogRef<UploadFileComponent>
  ) {}

  ngOnInit(): void {}

  public async onSubmit(forceOverwrite: boolean = false): Promise<void> {
    try {
      if (!this.selectedFile) return;
      // Build file path
      const filePath = `${
        this.authService.getUserInformation().username
      }/${this.driveService.getCurrentPath().join('/')}`;
      // Get file content
      const content = await this.selectedFile?.text();
      // Get file extension
      const extension =
        this.selectedFile.name.split('.').length > 1
          ? this.selectedFile.name.split('.')[1]
          : '';
      const newFileName = this.selectedFile.name.split('.')[0];
      await this.fileService.createFile({
        filePath,
        extension,
        newFileName,
        content,
        forceOverwrite,
      });
      this.snackBar.open('File uploaded!', 'Close', {
        verticalPosition: 'top',
        duration: 3000,
      });
      this.dialogRef.close(true);
    } catch (error: any) {
      const { requestOverrite } = error.error;
      if (!requestOverrite) {
        this.snackBar.open('Not enough space', 'Close', {
          verticalPosition: 'top',
          duration: 3000,
        });
        return;
      }
      this.isNameRepeated = true;
      console.log(error.error);
    }
  }

  public onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
  }

  public closeDialog() {
    this.dialogRef.close(false);
  }
}
