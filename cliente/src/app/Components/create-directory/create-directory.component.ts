import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { DirectoryService } from '../../Services/directory/directory.service';
import { DriveService } from '../../Services/drive/drive.service';
import { AuthenticationService } from '../../Services/authentication/authentication.service';

import { MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-create-directory',
  templateUrl: './create-directory.component.html',
  styleUrls: ['./create-directory.component.css'],
})
export class CreateDirectoryComponent implements OnInit {
  public directoryName: string = '';
  public isNameRepeated: boolean = false;

  public directoryNameFormControl: FormControl = new FormControl('', [
    Validators.required,
  ]);

  constructor(
    private directoryService: DirectoryService,
    private driveService: DriveService,
    private authService: AuthenticationService,
    private snackBar: MatSnackBar,
    public dialogRef: MatDialogRef<CreateDirectoryComponent>
  ) {}

  ngOnInit(): void {}

  public async onSubmit(
    overwriteDirectoryName: boolean = false
  ): Promise<void> {
    try {
      if (!this.directoryName) return;
      // Build request path
      const currentDirectoryPath = `${
        this.authService.getUserInformation().username
      }/${this.driveService.getCurrentPath().join('/')}`;
      // Create directory
      await this.directoryService.createDirectory(
        this.directoryName,
        currentDirectoryPath,
        overwriteDirectoryName
      );
      this.snackBar.open('Directory created!', 'Close', {
        verticalPosition: 'top',
        duration: 3000,
      });
      this.dialogRef.close(true);
    } catch (error: any) {
      this.isNameRepeated = true;
    }
  }

  public closeDialog() {
    this.dialogRef.close(false);
  }
}
