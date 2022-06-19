import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { SpaceAllocatorComponent } from './Components/space-allocator/space-allocator.component';
import { LoginComponent } from './Components/login/login.component';
import { DriveComponent } from './Components/drive/drive.component';
import { AuthenticationGuard } from './Guards/authentication.guard';

const routes: Routes = [
  { path: '', component: SpaceAllocatorComponent},
  {
    path: 'my-drive',
    component: DriveComponent,
    canActivate: [AuthenticationGuard],
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
