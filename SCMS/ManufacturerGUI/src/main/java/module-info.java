module com.example.manufacturergui {
    requires javafx.controls;
    requires javafx.fxml;
    requires lombok;
    requires java.desktop;
    requires okhttp3;
    requires com.fasterxml.jackson.databind;

    opens com.example.manufacturergui to javafx.fxml;
    opens com.example.manufacturergui.model to javafx.fxml;
    exports com.example.manufacturergui;
    exports com.example.manufacturergui.controller;
    exports com.example.manufacturergui.model;
    opens com.example.manufacturergui.controller to javafx.fxml;
}