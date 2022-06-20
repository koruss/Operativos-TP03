import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { SpaceAllocatorComponent } from './Components/space-allocator/space-allocator.component';
import { FileExplorerComponent } from './Components/file-explorer/file-explorer.component';

const routes: Routes = [
  { path: '', component: SpaceAllocatorComponent},
  {
    path: 'fs-explorer',
    component: FileExplorerComponent,
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
