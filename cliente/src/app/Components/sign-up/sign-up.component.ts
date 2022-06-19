import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthenticationService } from '../../Services/authentication/authentication.service';

import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';

import User from '../../Models/user.model';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css'],
})
export class SignUpComponent implements OnInit {
  public user: User = {
    username: '',
    password: '',
    allocatedBytes: 0,
  };
  public loginFormControl: FormControl = new FormControl('', [
    Validators.required,
  ]);
  public passwordFormControl: FormControl = new FormControl('', [
    Validators.required,
  ]);
  public sizeFormControl: FormControl = new FormControl('', [
    Validators.required,
  ]);

  constructor(
    private router: Router,
    private snackBar: MatSnackBar,
    private dialog: MatDialog,
    private authenticationService: AuthenticationService
  ) {}

  ngOnInit(): void {}

  public async onSignUpClick(): Promise<void> {
    try {
      // Validate input information
      if (
        !this.user.username ||
        !this.user.password ||
        !this.user.allocatedBytes
      ) {
        this.snackBar.open('Sign Up information not valid', 'Close', {
          verticalPosition: 'top',
          duration: 3000,
        });
        return;
      }
      await this.authenticationService.registerUser({
        ...this.user,
        requestedBytes: this.user.allocatedBytes,
      });
      // Store user profile information
      this.authenticationService.setIsAuthenticated(true);
      this.authenticationService.setUserInformation({
        username: this.user.username,
        allocatedBytes: this.user.allocatedBytes,
      });
      // Access drive
      this.snackBar.open(`Welcome ${this.user.username}!`, 'Close', {
        verticalPosition: 'top',
        duration: 3000,
      });
      this.dialog.closeAll();
      this.router.navigateByUrl('/my-drive');
    } catch (err: any) {
      const { message } = err.error;
      this.snackBar.open(message, 'Close', {
        verticalPosition: 'top',
        duration: 3000,
      });
    }
  }
}
