angular
	.module("remember.attachment")
	.controller("AttachmentController", AttachmentController);

AttachmentController.$inject = [
	"$scope", 
	"attachmentDataService", 
	"attachmentUploader", 
	"attachments", 
	"tags", 
	"$uibModal", 
	"$log", 
	"confirmModalService", 
	"alertService"
];

function AttachmentController($scope, attachmentDataService, attachmentUploader, attachments, tags, 
		$uibModal, $log, confirmModalService, alertService){
    $scope.attachments = attachments["attachments"];
    $scope.tags = tags["tags"];
    $scope.fileObjs = [];
    $scope.remveFileObj = function(index){
        $scope.fileObjs.splice(index, 1);
    };
    
    $scope.clearFileObjs = function(){
        $scope.fileObjs = [];
    };
    
    $scope.clearFilter = function(){
    	$scope.nameKey = "";
    	$scope.typeKey = "";
    	$scope.tagKey = "";
    };

    //listen for the file selected event
    $scope.$on("fileSelected", function (event, args) {
        $scope.$apply(function () {            
            //add the file object to the scope's files collection
            var fileObj = {
                "file": args.file,
                "status": "Pending",
                "tagInfo": {
                    "selectedTags": [],
                    "toggleSelection": function(id){
                        var index = this.selectedTags.indexOf(id);
                        if(index > -1){
                            this.selectedTags.splice(index, 1);
                        }
                        else{
                            this.selectedTags.push(id);
                        }
                    }
                }
            };
            
            $scope.fileObjs.push(fileObj);
        });
    });
    
    $scope.attachmentOperations = {
        "createAttachment": function(index){
            $scope.fileObjs[index].status = "loading";
            attachmentUploader($scope.fileObjs[index]).
                success(function(data){
                    $scope.attachments.push(data["attachment"]);
                    $scope.fileObjs[index].status = "success";
                }).
                error(function(){
                    $scope.fileObjs[index].status = "danger";
                });

        },
        "deleteAttachment": function(id, index){
            var modalOptions = {
                closeButtonText: "Cancel",
                actionButtonText: "Delete",
                headerText: "Delete " +$scope.attachments[index].name + "?",
                bodyText: "Are you sure you want to delete " + $scope.attachments[index].name +"?"
            };

            confirmModalService.showModal({}, modalOptions).then(function () {
            	attachmentDataService.delete({id: id}).$promise.then(
                    function(response){
                        $scope.attachments.splice(index, 1);
                        alertService.addAlert("success", "Success: attachment deleted!", 3000);
                    },
                    function(){
                        alertService.addAlert("danger", "Error: fail to delete attachment!", 3000);
                    }
                );
            }, function(){
                $log.info('Modal dismissed at: ' + new Date());
            });

        },
        "updateAttachment": function(index){
            var editAttachmentModalInstance = $uibModal.open({
                animation: true,
                templateUrl: "edit-attachment-modal",
                controller: "AttachmentEditModalController",
                size: "lg",
                resolve: {
                    attachment: function () {
                        return $scope.attachments[index];
                    }, 
                    tags: function(){
                        return $scope.tags;
                    }
                }
            });
    
            editAttachmentModalInstance.result.then(function (attachment) {
            	attachmentDataService.update({ id: attachment.id }, attachment).$promise.then(
                    function(response){
                        console.log(response);
                        $scope.attachments[index] = response["attachment"];
                        alertService.addAlert("success", "Success: attachment updated!", 3000);
                    },
                    function(){
                        alertService.addAlert("danger", "Error: fail to update attachment!", 3000);
                    }
                );
            }, function () {
                $log.info('Modal dismissed at: ' + new Date());
            });
        },
        "removeUnusedRow": function(index, attachment){
            if(attachment.id === -1){
                $scope.attachments.splice(index, 1);
            }
        }
    };

    
}