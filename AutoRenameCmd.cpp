#include <maya/MPxCommand.h>
#include <maya/MArgList.h>
#include <maya/MGlobal.h>
#include <maya/MSelectionList.h>
#include <maya/MObject.h>
#include <maya/MFnDagNode.h>
#include <maya/MStatus.h>

class AutoRenameCmd : public MPxCommand {
public:
    AutoRenameCmd() {}
    virtual MStatus doIt(const MArgList& args) override;
    static void* creator() { return new AutoRenameCmd(); }
};

// Command Execution
MStatus AutoRenameCmd::doIt(const MArgList& args) {
    MStatus status;

    // Get the prefix from arguments or set a default
    MString prefix = "object";
    if (args.length() > 0) {
        prefix = args.asString(0, &status);
        if (!status) {
            MGlobal::displayError("Invalid prefix argument.");
            return status;
        }
    }

    // Get the current selection
    MSelectionList selection;
    MGlobal::getActiveSelectionList(selection);
    if (selection.isEmpty()) {
        MGlobal::displayWarning("No objects selected!");
        return MS::kFailure;
    }

    // Iterate through selected objects and rename them
    for (unsigned int i = 0; i < selection.length(); ++i) {
        MObject obj;
        selection.getDependNode(i, obj);
        
        if (!obj.isNull()) {
            MFnDagNode dagNode(obj, &status);
            if (status == MS::kSuccess) {
                MString newName = prefix + "_" + MString(std::to_string(i + 1).c_str());
                dagNode.setName(newName);
            }
        }
    }

    MGlobal::displayInfo("Objects renamed successfully.");
    return MS::kSuccess;
}

// Plugin Registration
#include <maya/MFnPlugin.h>

MStatus initializePlugin(MObject obj) {
    MFnPlugin plugin(obj, "YourName", "1.0", "Any");
    return plugin.registerCommand("autoRename", AutoRenameCmd::creator);
}

MStatus uninitializePlugin(MObject obj) {
    MFnPlugin plugin(obj);
    return plugin.deregisterCommand("autoRename");
}
