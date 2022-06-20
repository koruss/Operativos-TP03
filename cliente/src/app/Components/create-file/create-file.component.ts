import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { FileService } from '../../Services/file/file.service';
import { DriveService } from '../../Services/drive/drive.service';

import { MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-create-file',
  templateUrl: './create-file.component.html',
  styleUrls: ['./create-file.component.css'],
})
export class CreateFileComponent implements OnInit {
  public fileName: string = '';
  public fileExtension: string = '';

  public fileNameFormControl: FormControl = new FormControl('', [
    Validators.required,
  ]);
  public fileExtensionFormControl: FormControl = new FormControl('', [
    Validators.required,
  ]);

  public isNameRepeated: boolean = false;

  constructor(
    private fileService: FileService,
    private driveService: DriveService,
    private snackBar: MatSnackBar,
    public dialogRef: MatDialogRef<CreateFileComponent>
  ) {}

  ngOnInit(): void {}

  public async onSubmit(forceOverwrite: boolean = false): Promise<void> {
    try {
      if (!this.fileName || !this.fileExtension) return;
      // Build request path
      let currentDirectoryPath = `${this.driveService.getCurrentPath().join('/')}`;
      if(currentDirectoryPath === ''){
        currentDirectoryPath = "root/";
      }
      await this.fileService.createFile({
        filePath: currentDirectoryPath,
        extension: this.fileExtension,
        newFileName: this.fileName,
        content: '',
        forceOverwrite,
      });
      this.snackBar.open('Archivo creado', 'Close', {
        verticalPosition: 'top',
        duration: 3000,
      });
      this.dialogRef.close(true);
    } catch (error: any) {
      console.log(error.error);
      this.isNameRepeated = true;
    }
  }

  public closeDialog() {
    this.dialogRef.close(false);
  }
}
